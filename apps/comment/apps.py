from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.comment'
    verbose_name = _("comment")
