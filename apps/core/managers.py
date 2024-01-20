from django.db import models


class LogicalQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_delete=True)

    def force_delete(self):
        return super().delete()
 

class LogicalManager(models.Manager):
    def get_queryset(self):
        return LogicalQuerySet(self.model, using=self._db).filter(is_delete=False)

    def archive(self):
        return LogicalQuerySet(self.model, using=self._db)

    def deleted(self):
        return LogicalQuerySet(self.model, using=self._db).filter(is_delete=True)
