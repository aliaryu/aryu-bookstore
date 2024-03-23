from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import (
    CustomUserManager,
    UserRelatedModelBaseManager
)
from .validators import (
    image_extension_validator,
    postal_code_validator,
)
from apps.core.models import LogicalBaseModel
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
import os, random


class User(AbstractUser):
    email = models.EmailField(
        verbose_name = _("email"),
        max_length = 255,
        unique = True,
    )
    birth_date = models.DateField(
        verbose_name = _("birth date"),
        blank = True,
        null = True,
    )
    is_active = models.BooleanField(
        verbose_name = _("active"),
        default = False,
        help_text = _(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    image = models.ImageField(
        verbose_name = _("image"),
        upload_to = "user_image/",
        blank = True,
        null = True,
        validators = [
            image_extension_validator
        ]
    )
    is_delete = models.BooleanField(
        verbose_name = _("delete"),
        default = False,
    )

    objects = CustomUserManager()

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError({'birth_date': _("birth date cannot be in future.")})

        width, height = self.image.width, self.image.height
        if width != height:
            raise ValidationError({'image': _("image must be square.")})

    def save(self, *args, **kwargs):
        if not self.image:
            image_folder = r"media\user-default"
            image_files = [img for img in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, img))]
            if image_files:
                random_image = random.choice(image_files)
                self.image = os.path.join("user-default", random_image)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def undelete(self):
        self.is_delete = False
        self.save()

    def force_delete(self):
        super().delete()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.username}"

    REQUIRED_FIELDS = ["email",]


class Address(models.Model):
    IRAN_PROVINCES = [
        ("AZR", "آذربایجان شرقی"),
        ("AZL", "آذربایجان غربی"),
        ("ARD", "اردبیل"),
        ("ESF", "اصفهان"),
        ("ALB", "البرز"),
        ("ILA", "ایلام"),
        ("BOS", "بوشهر"),
        ("TEH", "تهران"),
        ("CHR", "چهارمحال و بختیاری"),
        ("KHC", "خراسان رضوی"),
        ("KHT", "خراسان شمالی"),
        ("KHB", "خراسان جنوبی"),
        ("KHU", "خوزستان"),
        ("ZAN", "زنجان"),
        ("SEM", "سمنان"),
        ("SIS", "سیستان و بلوچستان"),
        ("FAR", "فارس"),
        ("QAZ", "قزوین"),
        ("QOM", "قم"),
        ("KOR", "کردستان"),
        ("KRN", "کرمان"),
        ("KRH", "کرمانشاه"),
        ("KOH", "کهگیلویه و بویراحمد"),
        ("GOL", "گلستان"),
        ("GIL", "گیلان"),
        ("LOR", "لرستان"),
        ("MAZ", "مازندران"),
        ("MAR", "مرکزی"),
        ("HOR", "هرمزگان"),
        ("HAM", "همدان"),
        ("YAZ", "یزد"),
    ]
    user = models.ForeignKey(
        verbose_name = _("user"),
        to = "User",
        on_delete = models.CASCADE,
    )
    province = models.CharField(
        verbose_name = _("province"),
        max_length = 3,
        choices = IRAN_PROVINCES,
        blank = False,
        null = False
    )
    postal_code = models.PositiveBigIntegerField(
        verbose_name = _("postal code"),
        validators = [postal_code_validator]
    )
    address_path = models.TextField(
        verbose_name = _("address")
    )

    objects = UserRelatedModelBaseManager()

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        return f"user: [ {self.user.username} ] - postal code: [ {self.postal_code} ]"
    
    def get_absolute_url(self):
        return reverse("user:useraddress", kwargs={"pk": self.pk})


class Role(LogicalBaseModel):
    ROLES = [
        ("M", "Manager"),
        ("S", "Supervisor"),
        ("O", "Operator"),
    ]
    role_name = models.CharField(
        verbose_name = _("role"),
        max_length = 1,
        choices = ROLES,
        unique = True,
    )
    salary = models.DecimalField(
        verbose_name = _("salary"),
        max_digits = 10,
        decimal_places = 2,
    )

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self):
        return f"{self.role_name}"


class Staff(models.Model):
    user = models.OneToOneField(
        verbose_name = _("user"),
        to = "User",
        on_delete = models.CASCADE,
    )
    role = models.ForeignKey(
        verbose_name = _("role"),
        to = "Role",
        on_delete = models.SET_NULL,
        null = True
    )

    objects = UserRelatedModelBaseManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.role.role_name == "M":
            group, created = Group.objects.get_or_create(name="Manager")
            if created:
                permissions_codenames = [
                    "add_book",
                    "change_book",
                    "delete_book",
                    "view_book",
                    "add_category",
                    "change_category",
                    "delete_category",
                    "view_category",
                    "add_discount",
                    "change_discount",
                    "delete_discount",
                    "view_discount",
                ]
                permissions = Permission.objects.filter(codename__in = permissions_codenames)
                group.permissions.add(*permissions)
            self.user.is_staff = True
            self.user.groups.set([group])
            self.user.save()

        elif self.role.role_name == "S":
            group, created = Group.objects.get_or_create(name="Supervisor")
            if created:
                permissions_codenames = [
                    "view_user",
                    "view_address",
                    "view_role",
                    "view_staff",
                    "view_author",
                    "view_genre",
                    "view_tag",
                    "view_category",
                    "view_book",
                    "view_discount",
                    "view_comment",
                    "view_order",
                    "view_orderbook",
                ]
                permissions = Permission.objects.filter(codename__in = permissions_codenames)
                group.permissions.add(*permissions)
            self.user.is_staff = True
            self.user.groups.set([group])
            self.user.save()
            
        elif self.role.role_name == "O":
            group, created = Group.objects.get_or_create(name="Operator")
            if created:
                permissions_codenames = [
                    "add_user",
                    "change_user",
                    "delete_user",
                    "view_user",
                    "add_address",
                    "change_address",
                    "delete_address",
                    "view_address",
                    "add_order",
                    "change_order",
                    "delete_order",
                    "view_order",
                    "add_orderbook",
                    "change_orderbook",
                    "delete_orderbook",
                    "view_orderbook",
                    "add_orderstaff",
                    "change_orderstaff",
                    "delete_orderstaff",
                    "view_orderstaff",
                ]
                permissions = Permission.objects.filter(codename__in = permissions_codenames)
                group.permissions.add(*permissions)
            self.user.is_staff = True
            self.user.groups.set([group])
            self.user.save()

    class Meta:
        verbose_name = _("staff")
        verbose_name_plural = _("staffs")

    def __str__(self):
        return f"{self.user.username}"
