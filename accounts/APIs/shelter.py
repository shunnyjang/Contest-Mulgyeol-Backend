from django.http import Http404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Shelter
from accounts.serializers import UserSerializer, ShelterSerializer
from config.permissions import IsOwnShelterOrReadOnly


class ShelterCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data.get('profile'))
        shelter = ShelterSerializer(data=request.data.get('shelter'))
        if user.is_valid():
            user.save()
            if shelter.is_valid():
                shelter.save()
                return Response({
                    "response": "success",
                    "message": "성공적으로 보호소를 등록했습니다."
                }, status=status.HTTP_201_CREATED)
            return Response({
                "response": "error",
                "message": shelter.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "response": "error",
            "message": user.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ShelterDetailView(APIView):
    permission_classes = [IsOwnShelterOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self, pk):
        try:
            return Shelter.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        shelter = self.get_object(pk)
        shelter_serializer = ShelterSerializer(shelter)
        return Response(shelter_serializer.data)

    def patch(self, request, pk, format=None):
        try:
            shelter = Shelter.objects.get(id=request.user.shelter.id)
        except:
            raise Http404

        shelter_serializer = ShelterSerializer(shelter, data=request.data, partial=True)
        if shelter_serializer.is_valid():
            shelter_serializer.save()
            return Response({
                "response": "success",
                "message": "성공적으로 수정하였습니다."})
        return Response({
            "response": "error",
            "message": shelter_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
