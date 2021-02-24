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
    text = models.CharField(max_length=32, null=True, verbose_name="태그명")

    def __str__(self):
        return self.text


class Recruitment(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    created_at = models.DateTimeField("업로드 날짜", auto_now=True)
    image = models.ImageField("첨부 이미지", upload_to=date_upload_to, null=True)
    information = models.TextField("봉사 설명", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="태그", related_name='recruitment')

    def __str__(self):
        return "[%s] %s 봉사모집" % (self.created_at, self.shelter)
        
    class Meta:
        ordering = ('-created_at',)


class DailyRecruitmentStatus(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False, default=timezone.now)
    need_number = models.PositiveIntegerField(default=9, verbose_name="필요한 인원")
    current_number = models.PositiveIntegerField(default=0, verbose_name="현재 인원")
    applicant = models.ManyToManyField(User)

    class Meta:
        def __str__(self):
            return "[%s]%s(%d/%d)" % (self.date, self.shelter.shelter_name, self.need_number, self.current_number)


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applying_for = models.ForeignKey(DailyRecruitmentStatus, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.user.name, self.applying_for)

    class Meta:
        unique_together = ['user', 'applying_for']
        ordering = ['-applied_at']
