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


class GenreModelTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            genre_name = 'Test Genre',
            description = 'This is a test genre',
        )

    def test_create_genre(self):
        self.assertEqual(self.genre.genre_name, 'Test Genre')
        self.assertEqual(self.genre.description, 'This is a test genre')

    def test_str_representation(self):
        self.assertEqual(str(self.genre), 'Test Genre')

    def test_unique_genre_name(self):
        with self.assertRaises(Exception):
            Genre.objects.create(genre_name = 'Test Genre')


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

    def test_image_field(self):
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


class BookTestCase(TestCase):
    def setUp(self):
        self.book = Book(
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
        test_image = SimpleUploadedFile("test_book_image.jpg", b"file_content", content_type="image/jpeg")
        self.book.image = test_image
        self.book.save()

    def tearDown(self):
        os.remove(self.book.image.path)

    def test_book_creation(self):
        self.assertEqual(self.book.book_name, "Book Name")
        self.assertEqual(self.book.publisher, "Publisher")
        self.assertEqual(self.book.description, "Description")
        self.assertEqual(self.book.excerpt, "Excerpt")
        self.assertEqual(self.book.pub_date, "1399-01-01")
        self.assertEqual(self.book.language, "Language")
        self.assertEqual(self.book.height, 200)
        self.assertEqual(self.book.width, 150)
        self.assertEqual(self.book.page, 300)
        self.assertEqual(self.book.count, 10)
        self.assertEqual(self.book.price, 200000.00)
    
    def test_image_field(self):
        self.assertIn("book_image/test_book_image", self.book.image.url)

    def test_str_representation(self):
        self.assertEqual(str(self.book), "Book Name - count: 10")

    def test_book_comments_relation(self):
        user = User.objects.create()
        comment = Comment.objects.create(
            user = user,
            text = 'Test Comment',
            content_object = self.book
        )
        self.assertIn(comment, self.book.comments.all())
