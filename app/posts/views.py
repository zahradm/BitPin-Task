from rest_framework.generics import CreateAPIView
from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.cache import cache
from app.posts.models import Post, Rating
from app.posts.serializers import PostListSerializer, PostSerializer
from app.posts.permissions import IsAdminUser


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
            rating_count=Count('ratings')
        )
        serializer = PostListSerializer(posts, many=True, context={'request': request})

        cache.set(cache_key, serializer.data, cache_timeout)

        return Response(serializer.data)


class PostRatingView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        score = request.data.get('score')

        if score is None or not (0 <= score <= 5):
            return Response({'detail': 'Invalid score. It should be between 0 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={'score': score}
        )

        cache.delete("post_list_with_ratings")

        return Response({'detail': 'Rating updated successfully.'}, status=status.HTTP_200_OK)


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        post = serializer.save()
        cache.delete("post_list_with_ratings")
