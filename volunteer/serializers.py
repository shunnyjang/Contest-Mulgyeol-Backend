from rest_framework import serializers
from volunteer.models import Post, Tag, Volunteer
from accounts.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'tag'
        ]

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'shelter',
            'created_at',
            'image',
            'information',
            'on_going'
        ]


class VolunteerSerializer(serializers.ModelSerializer):
    volunteers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Volunteer
        fields = [
            'shelter',
            'date',
            'limit_of_volunteer',
            'num_of_volunteer',
            'volunteers'
        ]