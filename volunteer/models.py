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

class Tag(models.Model):
    name = models.CharField(max_length=32, null=True, verbose_name="태그명")
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.name

class Post(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    created_at = models.DateTimeField("업로드 날짜", auto_now=True)
    image = models.ImageField("첨부 이미지", upload_to=date_upload_to, null=True)
    information = models.TextField("봉사 설명", blank=True)
    tag = models.ManyToManyField(Tag, verbose_name = "태그")

    def __str__(self):
        return "[%s] %s 봉사모집" % (self.created_at, self.shelter)
        
    class Meta:
        ordering = ('-created_at',)

class Volunteer(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    date = models.DateField()
    limit_of_volunteer = models.PositiveIntegerField(default=9)
    num_of_volunteer = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "[%s] %s" % (self.date, self.shelter.shelter_name)

    class Meta:
        ordering = ('-date',)

class UserVolunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.user.name, self.volunteer)

    class Meta:
        unique_together = ['user', 'volunteer']
        ordering = ['-applied_at']