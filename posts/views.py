from rest_framework.generics import CreateAPIView
from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from posts.models import Post, Rating
from posts.serializers import PostListSerializer, PostSerializer
from posts.permissions import IsAdminUser


class PostListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = Post.objects.annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings')
        )
        serializer = PostListSerializer(posts, many=True, context={'request': request})
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

        return Response({'detail': 'Rating updated successfully.'}, status=status.HTTP_200_OK)


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
