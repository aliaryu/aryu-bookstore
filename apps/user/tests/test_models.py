from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.user.models import Address, Staff, Role


class UserModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username = 'testuser',
            email = 'test@test.com',
            phone = '09180000000',
            password = 'password1234'
        )

    def test_create_user(self):
        self.user.full_clean()
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.phone, '09180000000',)
        self.assertTrue(self.user.check_password('password1234'))
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_delete)
        self.assertEqual(str(self.user), 'testuser')
    
    def test_delete_user(self):
        self.user.delete()
        self.assertTrue(self.user.is_delete)
        self.user.undelete()
        self.assertFalse(self.user.is_delete)
        self.user.force_delete()
        self.assertIsNone(self.User.objects.filter(username='testuser').first())


class AddressModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username = 'testuser',
            email = 'test@test.com',
            phone = '09180000000',
            password = 'password1234'
        )
        self.address = Address.objects.create(
            user = self.user,
            province = 'TEH',
            postal_code = 1234567890,
            address_path = 'test path'
        )

    def test_create_address(self):
        self.address.full_clean()
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.province, 'TEH')
        self.assertEqual(self.address.postal_code, 1234567890)
        self.assertEqual(self.address.address_path, 'test path')

    def test_address_str_method(self):
        expected_str = f"{self.address.id} - {self.address.postal_code}"
        self.assertEqual(str(self.address), expected_str)