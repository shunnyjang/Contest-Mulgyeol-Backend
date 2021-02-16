from django.contrib.auth import get_user_model
from django.http import Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.APIs.serializer_for_schema import ApiResponseSerializer
from community.models import Charity
from community.serializers import CharitySerializer
from config.permissions import IsAuthShelterOrReadOnly


class CharityView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]
    parser_classes = [FormParser, MultiPartParser]

    @extend_schema(
        description="보호소에서 업로드했던 후원내역 리스트를 반환하는 API입니다. query parameter로 shelter의 id를 포함하세요 (필수)",
        parameters=[OpenApiParameter("shelter", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True), ],
        responses={200: CharitySerializer}
    )
    def get(self, request):
        charity = Charity.objects.filter(shelter=request.query_params['shelter'])
        charity_serializer = CharitySerializer(charity, many=True)
        return Response(charity_serializer.data)

    @extend_schema(
        request=CharitySerializer,
        responses={201: ApiResponseSerializer,
                   400: ApiResponseSerializer}
    )
    def post(self, request):
        user = get_user_model().objects.get(pk=request.user.pk)
        shelter = user.shelter.pk
        request.data['shelter'] = shelter

        charity_serializer = CharitySerializer(data=request.data)
        if charity_serializer.is_valid():
            charity_serializer.save()
            return Response({
                "response": "success",
                "message": "성공적으로 후원내역 글을 업로드하였습니다."
            }, status=status.HTTP_201_CREATED)
        return Response({
            "response": "error",
            "message": charity_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CharityDetailView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]

    def get_object(self, pk):
        try:
            return Charity.objects.get(pk=pk)
        except:
            raise Http404

    @extend_schema(
        description="보호소에서 올린 커뮤니를 하나씩 보는 API입니다. 주소의 가장 마지막에 붙이는 숫자가 id인 모집 공고를 볼 수 있습니다.",
        responses=CharitySerializer
    )
    def get(self, request, pk, format=None):
        charity = self.get_object(pk)
        charity_serializer = CharitySerializer(charity)
        return Response(charity_serializer.data)

    @extend_schema(
        description="해당 커뮤니티 글을 부분적으로 수정할 수 있는 API입니다. image, content(글)를 수정할 수 있습니다.",
        request=CharitySerializer,
        responses={200: CharitySerializer,
                   400: ApiResponseSerializer}
    )
    def patch(self, request, pk, format=None):
        charity = self.get_object(pk)
        charity_serializer = CharitySerializer(charity,
                                               data=request.data,
                                               partial=True)
        if charity_serializer.is_valid():
            charity_serializer.save()
            return Response(charity_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'response': 'error',
            'message': charity_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="보호소에서 커뮤니티 포스트를 지우는 API입니다.",
        responses={204: None}
    )
    def delete(self, request, pk, format=None):
        charity = self.get_object(pk)
        charity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
