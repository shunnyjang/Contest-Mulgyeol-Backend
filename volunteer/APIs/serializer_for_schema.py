from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import serializers

from accounts.models import User
from volunteer.models import Tag, DailyRecruitmentStatus
from volunteer.serializers import TagSerializer


class VolunteerApplyReqeustSeriazlier(serializers.Serializer):
    shelter = serializers.CharField(required=True)
    date = serializers.DateField(required=True)

    class Meta:
        field = [
            'shelter',
            'date'
        ]


class RecruitmentSearchSerializer(serializers.Serializer):
    tag = serializers.CharField(required=False)
    location = serializers.CharField(required=False)

    class Meta:
        field = [
            'tag',
            'location'
        ]


class RecruitmentResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tags = TagSerializer(many=True)
    created_at = serializers.DateTimeField()
    image = serializers.ImageField()
    information = serializers.CharField()
    shelter = serializers.IntegerField()
    shelter_name = serializers.CharField()
    shelter_thumbnail = serializers.CharField()
    shelter_location = serializers.CharField()

    class Meta:
        field = '__all__'


class RecruitmentPostRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    information = serializers.CharField(required=False)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        required=True,
        slug_field='text'
    )
    start_date = serializers.DateField(required=True),
    end_date = serializers.DateField(required=True)

    class Meta:
        field = [
            'image',
            'information',
            'tags',
            'start_date',
            'end_date'
        ]


class DailyRecruitmentPostSerializer(serializers.Serializer):
    date = serializers.CharField(required=True)
    need_number = serializers.IntegerField(required=True)

    class Meta:
        field = [
            'shelter',
            'date',
            'need_number'
        ]


class DailyRecruitmentPostRequestSerializer(serializers.Serializer):
    available_date = DailyRecruitmentPostSerializer(many=True)

    class Meta:
        field = ['available_date']


class DailyRecruitmentPostResponeSerializer(serializers.Serializer):
    response = serializers.CharField()
    message = serializers.CharField()
    unavailable_date = serializers.DateField()

    class Meta:
        field = [
            'response',
            'message',
            'unavailable_date'
        ]


class DailyRecruitmentDetailRequestSerializer(serializers.Serializer):
    need_number = serializers.IntegerField(required=True)

    class Meta:
        field = ['need_number']


class VolunteerResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.IntegerField()
    applied_at = serializers.DateTimeField()
    applying_for = serializers.IntegerField()
    applying_date = serializers.DateField()
    shelter_name = serializers.CharField()
    shelter_chat_url = serializers.CharField()

    class Meta:
        field = '__all__'
