from django.contrib.auth.models import UserManager
from apps.core.managers import LogicalQuerySet, LogicalManager
from django.db import models


class CustomUserManager(UserManager, LogicalManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        return super().create_superuser(username, email, password, **extra_fields)


class UserRelatedModelBaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user__is_delete=False)
