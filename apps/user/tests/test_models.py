from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.user.models import Address, Staff, Role


class UserModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username = 'testuser',
            email = 'test@test.com',
            password = 'password1234'
        )

    def test_create_user(self):
        self.user.full_clean()
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertTrue(self.user.check_password('password1234'))
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
        expected_str = f"user: [ {self.user.username} ] - postal code: [ {self.address.postal_code} ]"
        self.assertEqual(str(self.address), expected_str)


class RoleModelTests(TestCase):
    def test_create_role(self):
        role = Role.objects.create(
            role_name = 'Operator',
            salary = 10000000.00
        )
        self.assertEqual(role.role_name, 'Operator')
        self.assertEqual(role.salary, 10000000.00)

    def test_role_str_method(self):
        role = Role.objects.create(
            role_name = 'Manager',
            salary = 20000000.00
        )
        expected_str = f"{role.role_name}"
        self.assertEqual(str(role), expected_str)


class StaffModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username = 'testuser',
            email = 'test@test.com',
            password = 'password1234'
        )
        self.role = Role.objects.create(
            role_name = 'Operator',
            salary = 10000000.00
        )

    def test_create_staff(self):
        staff = Staff.objects.create(
            user = self.user,
            role = self.role
        )
        self.assertEqual(staff.user, self.user)
        self.assertEqual(staff.role, self.role)

    def test_staff_str_method(self):
        staff = Staff.objects.create(
            user = self.user,
            role = self.role
        )
        expected_str = f"{staff.user.username}"
        self.assertEqual(str(staff), expected_str)