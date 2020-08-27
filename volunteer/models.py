from django.db import models
from accounts.models import Shelter, User

#image
import os
from uuid import uuid4
from django.db import models
from django.utils import timezone

def date_upload_to(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([ymd_path, uuid_name + extension, ])

class Post(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=date_upload_to)
    information = models.TextField(blank=True)
    on_going = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

class Tag(models.Model):
    tag = models.CharField("봉사 모집 태그", max_length=5)

    def __str__(self):
        return self.tag

class Volunteer(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    date = models.DateField()
    limit_of_volunteer = models.PositiveIntegerField(default=9)
    num_of_volunteer = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-date',)

class UserVolunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)