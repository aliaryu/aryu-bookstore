from django.contrib.auth.models import UserManager
from apps.core.managers import LogicalQuerySet
from django.db import models


class CustomUserManager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        return super().create_superuser(username, email, password, **extra_fields)

    def get_queryset(self):
        return LogicalQuerySet(self.model, using=self._db).filter(is_delete=False)

    def archive(self):
        return LogicalQuerySet(self.model, using=self._db)

    def deleted(self):
        return LogicalQuerySet(self.model, using=self._db).filter(is_delete=True)
    

class AddressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user__is_delete=False)