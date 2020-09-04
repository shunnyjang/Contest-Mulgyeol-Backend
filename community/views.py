from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from config.permissions import IsAuthShelter, IsAuthShelterOrReadOnly, IsOwnShelterOrReadOnly
from accounts.models import User, Shelter
from community.models import Community, Charity
from community.serializers import CommunitySerializer, CharitySerializer

from django.contrib.auth import get_user_model


# class ShelterView : accounts/view.py

class CommunityView(APIView):

    permission_classes = [IsAuthShelterOrReadOnly]
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, format=None):
        community = Community.objects.filter(shelter=request.query_params['shelter'])
        serializer = CommunitySerializer(community, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)

        request.data['shelter'] = request.user.shelter.pk

        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success",
                "message": "커뮤니티에 글을 등록하였습니다."
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "response": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)