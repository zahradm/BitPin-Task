from django.urls import path
from posts.views import PostListView, PostRatingView, PostCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:post_id>/', PostRatingView.as_view(), name='post-rating'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
]