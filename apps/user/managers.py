from typing import Any
from django.contrib.auth.models import UserManager
from apps.core.managers import LogicalQuerySet, LogicalManager
from django.db import models


class CustomUserManager(UserManager, LogicalManager):
    def create_user(self, username, email, password, **extra_fields):

        
        return super().create_user(username, email, password, **extra_fields)

    
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
