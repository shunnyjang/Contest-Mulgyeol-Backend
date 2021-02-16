from rest_framework import serializers

from accounts.models import Shelter
from community.models import Community, Charity, CharityImage


class CommunitySerializer(serializers.ModelSerializer):
    shelter = serializers.PrimaryKeyRelatedField(required=True, queryset=Shelter.objects.all())
    image = serializers.ImageField(required=False)
    content = serializers.CharField(required=False)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shelter_name'] = instance.shelter.shelter_name
        response['shelter_thumbnail'] = instance.shelter.thumbnail
        return response

    class Meta:
        model = Community
        fields = [
            'id',
            'shelter',
            'created_at',
            'image',
            'content'
        ]


class CharityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharityImage
        fields = [
            'image'
        ]


class CharitySerializer(serializers.ModelSerializer):
    shelter = serializers.PrimaryKeyRelatedField(required=False, queryset=Shelter.objects.all())
    images = CharityImageSerializer(many=True, read_only=True, required=False)
    content = serializers.CharField(required=False)

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        charity = Charity.objects.create(**validated_data)
        for image_data in images_data.getlist('image'):
            CharityImage.objects.create(charity=charity, image=image_data)
        return charity

    class Meta:
        model = Charity
        fields = '__all__'
