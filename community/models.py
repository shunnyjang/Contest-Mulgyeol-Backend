from django.db import models
from accounts.models import Shelter

# image
import os
from uuid import uuid4
from django.db import models
from django.utils import timezone


def date_upload_to(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([ymd_path, uuid_name + extension, ])


class Community(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, upload_to=date_upload_to)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

        def __str__(self):
            return "(%d) %s" % (self.shelter.shelter_name, self.created_at)


class Charity(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)


class CharityImage(models.Model):
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=date_upload_to)
