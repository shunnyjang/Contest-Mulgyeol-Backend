from rest_framework import serializers
from volunteer.models import Post, Tag, Volunteer, UserVolunteer
from accounts.models import User
from accounts.serializers import UserSerializer, ShelterSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'tag'
        ]

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shelter'] = ShelterSerializer(instance.shelter).data
        return response
    
    class Meta:
        model = Post
        fields = [
            'shelter',
            'created_at',
            'image',
            'information',
            'on_going',
            'tags'
        ]


class UserVolunteerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserVolunteer
        fields = [
            'id',
            'user',
            'volunteer'
        ]


class VolunteerSerializer(serializers.ModelSerializer):
    volunteers = UserVolunteerSerializer(many=True, read_only=True)

    class Meta:
        model = Volunteer
        fields = [
            'id',
            'shelter',
            'date',
            'limit_of_volunteer',
            'num_of_volunteer',
            'volunteers'
        ]
