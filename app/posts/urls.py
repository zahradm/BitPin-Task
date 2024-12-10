from django.urls import path
from app.posts.views import PostListView, PostRatingView, PostCreateView

urlpatterns = [
    path('list/', PostListView.as_view(), name='post-list'),
    path('rate/<int:post_id>/', PostRatingView.as_view(), name='post-rating'),
    path('create/', PostCreateView.as_view(), name='post-create'),
]