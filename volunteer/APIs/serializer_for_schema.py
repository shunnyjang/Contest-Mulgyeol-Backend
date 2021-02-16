from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import serializers
from volunteer.models import Tag


class VolunteerApplyReqeustSeriazlier(serializers.Serializer):
    shelter = serializers.CharField(required=True)
    date = serializers.DateField(required=True)

    class Meta:
        field = [
            'shelter',
            'date'
        ]


class RecruitmentSearchSerializer(serializers.Serializer):
    tags = serializers.CharField()

    class Meta:
        field = [
            'tags'
        ]


class RecruitmentPostRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    information = serializers.CharField(required=False)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        required=True,
        slug_field='text'
    )

    class Meta:
        field = [
            'image',
            'information',
            'tags'
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
