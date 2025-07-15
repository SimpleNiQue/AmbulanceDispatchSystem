import uuid

from django.db import models


class Audit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Description(models.Model):
    short_description = models.CharField(max_length=255, null=True)
    long_description = models.TextField(null=True)

    class Meta:
        abstract = True
