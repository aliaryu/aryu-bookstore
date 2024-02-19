from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.product.models import (
    Category,
    Genre,
    Tag,
    Author,
    Book
)
from apps.comment.models import Comment
from django.contrib.auth import get_user_model
import os


User = get_user_model()


class CategoryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            cat_name = 'Test Category',
        )

    def test_create_category(self):
        self.assertEqual(self.category.cat_name, 'Test Category')
        self.assertIsNone(self.category.cat_parent)
        with self.assertRaises(ValueError):
            self.category.image.url

    def test_str_representation(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_unique_cat_name(self):
        with self.assertRaises(Exception):
            Category.objects.create(cat_name = 'Test Category')

    def test_cat_parent(self):
        parent_category = Category.objects.create(cat_name = 'Parent Category')
        self.category.cat_parent = parent_category
        self.category.save()
        self.assertEqual(self.category.cat_parent, parent_category)

    def test_image_field(self):
        test_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type = "image/jpeg")
        self.category.image = test_image
        self.category.save()
        self.assertIn("category_image/test_image", self.category.image.url)
        os.remove(self.category.image.path)


class GenreModelTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            genre_name = 'Test Genre',
            description = 'This is a test genre',
        )

    def test_create_genre(self):
        self.assertEqual(self.genre.genre_name, 'Test Genre')
        self.assertEqual(self.genre.description, 'This is a test genre')
        with self.assertRaises(ValueError):
            self.genre.image.url

    def test_str_representation(self):
        self.assertEqual(str(self.genre), 'Test Genre')

    def test_unique_genre_name(self):
        with self.assertRaises(Exception):
            Genre.objects.create(genre_name = 'Test Genre')

    def test_image_field(self):
        test_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.genre.image = test_image
        self.genre.save()
        self.assertIn("genre_image/test_image", self.genre.image.url)
        os.remove(self.genre.image.path)


class TagModelTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(
            tag_name = 'Test Tag'
        )

    def test_create_tag(self):
        self.assertEqual(self.tag.tag_name, 'Test Tag')

    def test_str_representation(self):
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_unique_tag_name(self):
        with self.assertRaises(Exception):
            Tag.objects.create(tag_name='Test Tag')


class AuthorModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            full_name = 'Test Author',
            biography = 'This is a test biography',
            brief = 'This is a test brief',
            nationality = 'Test Nationality',
        )

    def test_create_author(self):
        self.assertEqual(self.author.full_name, 'Test Author')
        self.assertEqual(self.author.biography, 'This is a test biography')
        self.assertEqual(self.author.brief, 'This is a test brief')
        self.assertEqual(self.author.nationality, 'Test Nationality')
        with self.assertRaises(ValueError):
            self.author.image.url

    def test_author_image_upload(self):
        test_image = SimpleUploadedFile("test_author_image.jpg", b"file_content", content_type="image/jpeg")
        self.author.image = test_image
        self.author.save()
        self.assertIn("author_image/test_author_image", self.author.image.url)
        os.remove(self.author.image.path)

    def test_author_comments_relation(self):
        user = User.objects.create()
        comment = Comment.objects.create(
            user = user,
            text = 'Test Comment',
            content_object = self.author
        )
        self.assertIn(comment, self.author.comments.all())