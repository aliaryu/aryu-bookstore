from django.db import models
from .managers import LogicalManager
from django.utils.translation import gettext_lazy as _


class LogicalBaseModel(models.Model):
    is_delete = models.BooleanField(
        verbose_name = _("delete"),
        default = False
    )

    objects = LogicalManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def undelete(self):
        self.is_delete = False
        self.save()

    def force_delete(self):
        super().delete()


class TimeStampBaseModel(models.Model):
    create_at = models.DateTimeField(
        verbose_name = _("create at"),
        auto_now_add = True,
    )
    update_at = models.DateTimeField(
        verbose_name = _("update at"),
        auto_now = True,
    )

    class Meta:
        abstract = True