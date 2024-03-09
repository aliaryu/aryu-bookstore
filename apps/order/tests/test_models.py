from django.test import TestCase
from apps.order.models import Order, OrderBook
from apps.product.models import Book
from apps.user.models import Address, Staff, Role
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            password = "testpassword"
        )
        self.address = Address.objects.create(
            user = self.user,
            province = "TEH",
            postal_code = "1234567890",
            address_path = "Iran - Ilam"
        )
        self.book = Book.objects.create(
            book_name = "Test Book",
            publisher = "Test Publisher",
            description = "Test Description",
            excerpt = "Test Excerpt",
            pub_date = "1399-01-01",
            language = "Test Language",
            height = 200,
            width = 150,
            page = 300,
            count = 10,
            price = 200000.00,
        )
        self.role = Role.objects.create(
            role_name = "Test",
            salary = 50000000.00
        )
        self.staff = Staff.objects.create(
            user = self.user,
            role = self.role
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user = self.user,
            address = self.address,
            staff = self.staff,
        )
        orderbook = OrderBook.objects.create(
            order = order,
            book = self.book,
            count = 1
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.address, self.address)
        self.assertEqual(order.staff, self.staff)
        self.assertEqual(order.status, "PEN")
        self.assertIn(orderbook, order.orderbook_set.all())

    def test_order_str_representation(self):
        order = Order.objects.create(
            user = self.user,
            address = self.address,
            staff =self.staff,
        )
        expected_str = f"order number: [ {order.id} ]"
        self.assertEqual(str(order), expected_str)


class OrderBookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            password = "testpassword"
        )
        self.address = Address.objects.create(
            user = self.user,
            province = "TEH",
            postal_code = "1234567890",
            address_path = "Iran - Ilam"
        )
        self.book = Book.objects.create(
            book_name = "Test Book",
            publisher = "Test Publisher",
            description = "Test Description",
            excerpt = "Test Excerpt",
            pub_date = "1399-01-01",
            language = "Test Language",
            height = 200,
            width = 150,
            page = 300,
            count = 10,
            price = 200000.00,
        )
        self.order = Order.objects.create(
            user = self.user,
            address = self.address,
        )

    def test_order_book_creation(self):
        order_book = OrderBook.objects.create(
            order = self.order,
            book = self.book,
            count = 1
        )
        self.assertEqual(order_book.order, self.order)
        self.assertEqual(order_book.book, self.book)
        self.assertEqual(order_book.count, 1)

    def test_order_book_clean_method(self):
        with self.assertRaises(Exception):
            order_book = OrderBook.objects.create(
                order = self.order,
                book = self.book,
                count = 15
            )
            order_book.full_clean()

    def test_order_book_save_method(self):
        order_book = OrderBook.objects.create(
            order = self.order,
            book = self.book,
            count = 3
        )
        book_count = Book.objects.get(id = self.book.id).count
        self.assertEqual(book_count, 7)