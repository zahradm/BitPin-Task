from rest_framework import serializers
from app.posts.models import Post, Rating


class PostListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField()
    rating_count = serializers.IntegerField()
    user_score = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'avg_rating', 'rating_count', 'user_score']

    def get_user_score(self, obj):
        user = self.context['request'].user
        rating = obj.ratings.filter(user=user).first()
        return rating.score if rating else None


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content']
