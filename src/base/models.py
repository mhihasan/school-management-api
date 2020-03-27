from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.now()
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class TimeStampIndexedModel(models.Model):
    date_created = models.DateTimeField(blank=True, null=True, db_index=True)
    last_updated = models.DateTimeField(blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.now()
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
