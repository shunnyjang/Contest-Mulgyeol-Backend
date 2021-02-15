from rest_framework import serializers

from accounts.serializers import UserSerializer, ShelterSerializer


class ApiResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    message = serializers.CharField()

    class Meta:
        field = [
            'response',
            'message'
        ]


class CheckIdRequestSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)

    class Meta:
        field = ['id']


class SignInRequestSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        field = [
            'userID',
            'password'
        ]


class SignInResponseSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)

    class Meta:
        field = ['token']


class ShelterCreateRequestSerializer(serializers.Serializer):
    profile = UserSerializer()
    shelter = ShelterSerializer()

    class Meta:
        field = [
            'profile',
            'shelter'
        ]
