from rest_framework import serializers
from volunteer.models import Recruitment, DailyRecruitmentStatus, Volunteer, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'text'
        ]


class RecruitmentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False, many=True, read_only=True)

    def create(self, validated_data):
        return Recruitment.objects.create(**validated_data)

    class Meta:
        model = Recruitment
        fields = '__all__'


class DailyRecruitmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecruitmentStatus
        fields = '__all__'


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'
