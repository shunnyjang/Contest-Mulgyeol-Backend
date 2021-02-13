from rest_framework import serializers
from accounts.models import User, Shelter, PhoneAuth


class UserSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'

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
        fields = '__all__'


class PhoneAuthSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    auth_number = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = PhoneAuth
        fields = [
            'phone_number',
            'auth_number'
        ]
