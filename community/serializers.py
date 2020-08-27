from rest_framework import serializers
from community.models import Community, Charity, CharityImage


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
