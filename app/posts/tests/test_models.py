from django.test import TestCase
from app.users.models import User
from app.posts.models import Post, Rating


class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Test Post", content="This is a test post.")

    def test_post_creation(self):
        """Test that a Post instance can be created successfully."""
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post.")

    def test_post_str(self):
        """Test the __str__ method of the Post model."""
        self.assertEqual(str(self.post), "Test Post")


class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.post = Post.objects.create(title="Test Post", content="This is a test post.")
        self.rating = Rating.objects.create(user=self.user, post=self.post, score=5)

    def test_rating_creation(self):
        """Test that a Rating instance can be created successfully."""
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(self.rating.user, self.user)
        self.assertEqual(self.rating.post, self.post)
        self.assertEqual(self.rating.score, 5)

    def test_rating_unique_constraint(self):
        """Test that the unique_together constraint works for Rating."""
        with self.assertRaises(Exception):  # Expecting IntegrityError
            Rating.objects.create(user=self.user, post=self.post, score=3)

    def test_rating_related_name(self):
        """Test the related_name on the Rating model."""
        self.assertEqual(self.post.ratings.count(), 1)
        self.assertEqual(self.post.ratings.first(), self.rating)
