from rest_framework import serializers
from community.models import Community, Charity, CharityImage

class CommunitySerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shelter_name'] = instance.shelter.shelter_name
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

class CharityImageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharityImage
        fields = [
            'charity',
            'image'
        ]


class CharitySerializer(serializers.ModelSerializer):
    images = CharityImageImageSerializer(many=True, read_only=True)

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        charity = Charity.objects.create(**validated_data)
        
        for image_data in images_data.getlist('image'):
            CharityImage.objects.create(charity=charity, image=image_data)
        return charity

    class Meta:
        model = Charity
        fields = [
            'shelter',
            'created_at',
            'content',
            'images'
        ]
