from rest_framework import serializers
from volunteer.models import Post, Tag, Volunteer, UserVolunteer
from accounts.models import User
from accounts.serializers import UserSerializer, ShelterSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name'
        ]

class PostSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shelter'] = ShelterSerializer(instance.shelter).data
        response['tags'] = TagSerializer(instance.tag, many=True, read_only=True).data
        return response
    
    class Meta:
        model = Post
        fields = [
            'id',
            'shelter',
            'created_at',
            'image',
            'information',
        ]


class UserVolunteerSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['volunteer'] = VolunteerSerializer(instance.volunteer).data
        return response

    class Meta:
        model = UserVolunteer
        fields = [
            'id',
            'applied_at',
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
