from django.db import models
from app.users.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'post')

