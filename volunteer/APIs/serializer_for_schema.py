from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import serializers
from volunteer.models import Tag


class VolunteerApplyReqeustSeriazlier(serializers.Serializer):
    shelter = serializers.CharField(required=True)
    date = serializers.DateField(required=True)

    class Meta:
        field = [
            'shelter',
            'date'
        ]


class RecruitmentSearchSerializer(serializers.Serializer):
    tags = serializers.CharField()

    class Meta:
        field = [
            'tags'
        ]


class RecruitmentPostRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    information = serializers.CharField(required=False)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        required=True,
        slug_field='text'
    )

    class Meta:
        field = [
            'image',
            'information',
            'tags'
        ]


class JWTTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework_jwt.authentication.JSONWebTokenAuthentication'
    name = 'tokenAuth'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        if self.target.keyword == 'Bearer':
            return {
                'type': 'http',
                'scheme': 'bearer',
            }
        else:
            return {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': _(
                    'Token-based authentication with required prefix "%s"'
                ) % self.target.keyword
            }
