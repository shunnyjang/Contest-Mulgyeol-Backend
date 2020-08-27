from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from accounts.models import User, Shelter

User = get_user_model()

class UserSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    class Meta:
        fields = [
            'id',
            'userID',
            'name',
            'phone',
            'role'
        ]

    def create(self, validated_data):
        user = User.objects.create(
            userID=validated_data['userID'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class ShelterSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='userID')

    class Meta:
        model = Shelter
        fields = [
            'id',
            'user',
            'shelter_name',
            'loc_short',
            'loc_detail',
            'url',
            'chat_url',
            'status',
            'content',
            'caution'
        ]