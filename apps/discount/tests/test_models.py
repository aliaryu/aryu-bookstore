from django.test import TestCase
from apps.discount.models import Discount
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class DiscountTestCase(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            percent = 10,
            maximum = 100,
            expire_date = timezone.now() + timedelta(days=30)
        )

    def test_discount_creation(self):
        self.assertEqual(self.discount.percent, 10)
        self.assertEqual(self.discount.maximum, 100)

    def test_discount_clean_method(self):
        with self.assertRaises(ValidationError):
            discount = Discount.objects.create(
                percent = 20,
                cash = 50,
                maximum = 200,
                expire_date = timezone.now() + timedelta(days=30)
            )
            discount.full_clean()
        with self.assertRaises(ValidationError):
            discount = Discount.objects.create(
                maximum = 200,
                expire_date = timezone.now() + timedelta(days=30)
            )
            discount.full_clean()

    def test_discount_save_method(self):
        self.assertIsNotNone(self.discount.code)

    def test_discount_str_representation(self):
        expected_str = "code: {} - percent: {} %".format(self.discount.code, self.discount.percent)
        self.assertEqual(str(self.discount), expected_str)