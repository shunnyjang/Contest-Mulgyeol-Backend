from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# SMS 인증
from model_utils.models import TimeStampedModel
from random import randint
from accounts.utils import send_sms

# thumbnail
import os
from uuid import uuid4
from django.db import models
from django.utils import timezone


def date_upload_to(instance, filename):
    # ymd_path = timezone.now().strftime('%Y/%m/%d')
    path = "shelter" + str(instance.pk) + "_thumbnail"
    extension = os.path.splitext(filename)[-1].lower()
    return path + extension


def thumbnail_upload_to(instance):
    shelter = instance.user.userID
    return "%s.png" % shelter


class UserManager(BaseUserManager):
    user_in_migrations = True

    def _create_user(self, userID, password=None, **extra_fields):
        if not userID:
            raise ValueError('아이디를 입력하세요.')
        user = self.model(userID=userID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, userID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(userID, password, **extra_fields)

    def create_superuser(self, userID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(userID, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    ROLE_CHOICES = (
        ('1', '봉사자'),
        ('2', '보호소 담당자'),
    )
    
    userID = models.CharField(max_length=21, blank=False, unique=True)
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11, blank=False, unique=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'userID'

    def __str__(self):
        return "[%s] %s" % (self.role, self.userID)


class Shelter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shelter')
    shelter_name = models.CharField("보호소 이름", max_length=20)
    loc_short = models.CharField("간단한 주소", max_length=15, default="서울특별시 종로구")
    loc_detail = models.CharField("상세 주소", max_length=50, blank=True)
    thumbnail = models.ImageField("첨부 이미지", upload_to=date_upload_to, null=True)
    url = models.CharField("보호소 홍보 SNS URL", max_length=200, blank=True)
    chat_url = models.CharField("보호소 오픈채팅 URL", max_length=200, blank=True)
    status = models.CharField("동물 보호 현황", max_length=100, null=False, default="개 0마리")
    content = models.TextField("보호소 소개", blank=True)
    caution = models.TextField("봉사 주의사항", blank=True)

    def __str__(self):
        return "(%d)[%s] %s" % (self.id, self.loc_short, self.shelter_name)
    
    @property
    def is_shelter_staff(self):
        return self.user.role == '2'


class PhoneAuth(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)
        send_sms(auth_number=self.auth_number, phone_number=self.phone_number)

    class Meta:
        def __init__(self):
            self.auth_number = None
            self.phone_number = None

        def __str__(self):
            return "%s[%s]" % (self.phone_number, self.auth_number)
