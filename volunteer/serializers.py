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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shelter_name'] = instance.shelter.shelter_name
        response['shelter_thumbnail'] = str(instance.shelter.thumbnail)
        return response

    class Meta:
        model = Recruitment
        fields = '__all__'


class DailyRecruitmentStatusSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.need_number = validated_data.get('need_number', instance.need_number)
        instance.save()
        return instance

    class Meta:
        model = DailyRecruitmentStatus
        fields = [
            "id",
            "shelter",
            "date",
            "need_number",
            "current_number",
        ]


class DailyRecruitmentVolunteerSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField(many=True)

    class Meta:
        model = DailyRecruitmentStatus
        fields = [
            "id",
            "shelter",
            "date",
            "need_number",
            "current_number",
            'applicant'
        ]


class VolunteerSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Volunteer.objects.create(**validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['applying_date'] = instance.applying_for.date
        response['shelter_name'] = instance.applying_for.shelter.shelter_name
        response['shelter_chat_url'] = instance.applying_for.shelter.chat_url
        return response

    class Meta:
        model = Volunteer
        fields = '__all__'
