from django.core.cache import cache
from django.db.models import Avg, Count, StdDev
from django.shortcuts import get_object_or_404
from django_redis import get_redis_connection

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.posts.models import Post, Rating
from app.posts.permissions import IsAdminUser
from app.posts.serializers import PostListSerializer, PostSerializer


class PostListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cache_key = "post_list_with_ratings"
        cache_timeout = 60 * 5
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        posts = Post.objects.annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings'),
            rating_std_dev=StdDev('ratings__score')
        )

        for post in posts:
            if post.rating_std_dev is not None and post.rating_std_dev < 1:
                post.avg_weighted_rating = post.avg_rating * 0.5
            else:
                post.avg_weighted_rating = post.avg_rating

        serializer = PostListSerializer(posts, many=True, context={'request': request})

        cache.set(cache_key, serializer.data, cache_timeout)

        return Response(serializer.data)


class PostRatingView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        user = request.user
        score = request.data.get('score')
        post = get_object_or_404(Post, id=post_id)

        if score is None or not (0 <= score <= 5):
            return Response({'detail': 'Invalid score. It should be between 0 and 5.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if self.is_rate_limited(user, post_id):
            return Response({'detail': 'You have already rated this post recently.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        rating, created = Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={'score': score}
        )

        cache.delete("post_list_with_ratings")

        return Response({'detail': 'Rating updated successfully.'}, status=status.HTTP_200_OK)


    def is_rate_limited(self, user, post_id):
        redis = get_redis_connection('default')
        key = f"rate_limit_{post_id}_user_{user.id}"
        if redis.get(key):
            return True
        redis.setex(key, 60, "1")
        return False


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        post = serializer.save()
        cache.delete("post_list_with_ratings")
