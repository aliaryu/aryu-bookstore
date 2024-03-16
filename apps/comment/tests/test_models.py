from django.test import TestCase
from apps.comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from apps.product.models import Book
from django.contrib.auth import get_user_model


User = get_user_model()


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            password = "testpassword",
            email = "test@test.com"
        )
        self.content_type = ContentType.objects.create(model = "test_model")
        self.object_id = 1

    def test_comment_creation(self):
        comment = Comment.objects.create(
            user = self.user,
            text = "This is a comment",
            content_type = self.content_type,
            object_id = self.object_id,
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.text, "This is a comment")
        self.assertEqual(comment.content_type, self.content_type)
        self.assertEqual(comment.object_id, self.object_id)

    def test_comment_assign(self):
        book = Book.objects.create(
            book_name = "Book Name",
            publisher = "Publisher",
            description = "Description",
            excerpt = "Excerpt",
            pub_date = "1399-01-01",
            language = "Language",
            height = 200,
            width = 150,
            page = 300,
            count = 10,
            price = 200000.00,
        )
        comment = Comment.objects.create(
            user = self.user,
            text = 'Test Comment',
            content_object = book
        )
        self.assertIn(comment, book.comments.all())

    def test_comment_str_representation(self):
        comment = Comment.objects.create(
            user = self.user,
            text = "This is a comment",
            content_type = self.content_type,
            object_id = self.object_id,
        )
        expected_str = f"{self.user.username} - This is a "
        self.assertEqual(str(comment), expected_str)
