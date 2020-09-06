from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# SMS 인증
from model_utils.models import TimeStampedModel
from random import randint
import time
import requests
import hashlib
import hmac
import base64
import json
from config.settings.base import SMS_ACCESS_KEY, SMS_SECRET_KEY, SMS_SERVICE_ID, SMS_FROM_NUMBER

# thumbnail
import os
from uuid import uuid4
from django.db import models
from django.utils import timezone

def date_upload_to(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([ymd_path, uuid_name + extension, ])


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
    url = models.CharField("보호소 홍보 SNS URL", max_length=200, blank=True)
    chat_url = models.CharField("보호소 오픈채팅 URL", max_length=200, blank=True)
    status = models.CharField("동물 보호 현황", max_length=100, null=False, default="개 0마리")
    content = models.TextField("보호소 소개", blank=True)
    caution = models.TextField("봉사 주의사항", blank=True)

    def __str__(self):
        return "[%s] %s" % (self.loc_short, self.shelter_name)
    
    @property
    def is_shelter_staff(self):
        return self.user.role == '2'

class ShelterThumbnail(models.Model):
    shelter = models.OneToOneField(Shelter, on_delete=models.CASCADE)
    thumbnail = models.ImageField(null=True, upload_to=date_upload_to)

class PhoneAuth(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_sms()
    
    def	make_signature(self, access_key, secret_key, timestamp):
        method = "POST"
        uri = "/sms/v2/services/%s/messages" % (SMS_SERVICE_ID)

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey
    
    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        access_key = SMS_ACCESS_KEY
        secret_key = SMS_SECRET_KEY
        secret_key = bytes(secret_key, 'UTF-8')
        signature = self.make_signature(access_key, secret_key, timestamp)

        url = "https://sens.apigw.ntruss.com/sms/v2/services/%s/messages" % (SMS_SERVICE_ID)
        content = {
            "type": "SMS",
            "from": SMS_FROM_NUMBER,
            "content": "[테스트] 인증 번호 [%d]를 입력해주세요." % (self.auth_number),
            "messages":[
                {
                    "to": self.phone_number
                }
            ]
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signature
        }
        res = requests.post(url, headers=headers, data=json.dumps(content))
        
    class Meta:
        def __str__(self):
            return "%s[%s]" % (self.phone_number, self.auth_number)