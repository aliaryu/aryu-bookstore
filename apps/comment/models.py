from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import LogicalBaseModel, TimeStampBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


User = get_user_model()


class Comment(LogicalBaseModel, TimeStampBaseModel):

    # Fields

    user = models.ForeignKey(
        verbose_name = _("user"),
        to = User,
        on_delete = models.CASCADE,
    )
    text = models.TextField(
        verbose_name = _("text"),
    )
    answer = models.TextField(
        verbose_name = _("answer"),
        blank = True,
        null = True,
    )
    approve = models.BooleanField(
        verbose_name = _("approve"),
        default = False,
    )

    # Generic Relation

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return f"{self.user.username} - {self.text[:10]}"
