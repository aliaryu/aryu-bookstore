from typing import Any
from django.contrib.auth.models import UserManager
from apps.core.managers import LogicalManager
from django.db import models
from config import settings



class CustomUserManager(UserManager, LogicalManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        if settings.DEBUG:
            extra_fields.setdefault("is_active", True)

        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class UserRelatedModelBaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user__is_delete=False)
