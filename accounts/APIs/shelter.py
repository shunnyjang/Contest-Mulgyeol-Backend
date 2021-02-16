from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.APIs.serializer_for_schema import ShelterCreateRequestSerializer, ApiResponseSerializer
from accounts.models import Shelter
from accounts.serializers import UserSerializer, ShelterSerializer
from config.permissions import IsAuthShelterOrReadOnly


class ShelterCreateView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ShelterCreateRequestSerializer,
        responses={200: ApiResponseSerializer,
                   400: ApiResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data.get('profile'))
        shelter = ShelterSerializer(data=request.data.get('shelter'))
        if user.is_valid():
            user_instance = user.save()
            if shelter.is_valid():
                shelter.save()
                return Response({
                    "response": "success",
                    "message": "성공적으로 보호소를 등록했습니다."
                }, status=status.HTTP_201_CREATED)
            user_instance.delete()
            return Response({
                "response": "error",
                "message": shelter.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "response": "error",
            "message": user.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ShelterDetailView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self, pk):
        try:
            return Shelter.objects.get(pk=pk)
        except:
            raise Http404

    @extend_schema(
        responses=ShelterSerializer
    )
    def get(self, request, pk, format=None):
        shelter = self.get_object(pk)
        shelter_serializer = ShelterSerializer(shelter)
        return Response(shelter_serializer.data)

    @extend_schema(
        description="보호소 정보를 부분적으로 수정할 수 있는 API입니다. 수정하고자 하는 것만 request body로 포함하면 됩니다.",
        request=ShelterSerializer,
        responses={200: ApiResponseSerializer,
                   400: ApiResponseSerializer}
    )
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
                "message": "성공적으로 수정하였습니다."}, status=status.HTTP_200_OK)
        return Response({
            "response": "error",
            "message": shelter_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
