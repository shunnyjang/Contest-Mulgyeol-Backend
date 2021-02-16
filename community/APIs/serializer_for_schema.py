from rest_framework import serializers


class CommunityPostRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        fields = [
            'image',
            'content'
        ]
