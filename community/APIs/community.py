from django.contrib.auth import get_user_model
from django.http import Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.APIs.serializer_for_schema import ApiResponseSerializer
from community.APIs.serializer_for_schema import CommunityPostRequestSerializer
from community.models import Community
from community.serializers import CommunitySerializer
from config.permissions import IsAuthShelterOrReadOnly


class CommunityView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]
    parser_classes = [FormParser, MultiPartParser]

    @extend_schema(
        description="보호소에서 업로드했던 커뮤니티 글 (보호소 일상 글) 리스트를 반환하는 API입니다. query parameter로 shelter의 id를 포함하세요 (필수)",
        parameters=[OpenApiParameter("shelter", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),],
        responses=CommunitySerializer
    )
    def get(self, request, format=None):
        community = Community.objects.filter(shelter=request.query_params['shelter'])
        serializer = CommunitySerializer(community, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="보호소에서 커뮤니티 글을 업로드하는 API입니다.",
        request=CommunityPostRequestSerializer,
        responses=CommunitySerializer
    )
    def post(self, request, format=None):
        user = get_user_model().objects.get(pk=request.user.pk)
        request.data['shelter'] = user.shelter.pk

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


class CommunityDetailView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]

    def get_object(self, pk):
        try:
            return Community.objects.get(pk=pk)
        except:
            raise Http404

    @extend_schema(
        description="보호소에서 올린 커뮤니를 하나씩 보는 API입니다. 주소의 가장 마지막에 붙이는 숫자가 id인 모집 공고를 볼 수 있습니다.",
        responses=CommunitySerializer
    )
    def get(self, request, pk, format=None):
        community = self.get_object(pk)
        community_serializer = CommunitySerializer(community)
        return Response(community_serializer.data)

    @extend_schema(
        description="해당 커뮤니티 글을 부분적으로 수정할 수 있는 API입니다. image, content(글)를 수정할 수 있습니다.",
        request=CommunitySerializer,
        responses={200: CommunitySerializer,
                   400: ApiResponseSerializer}
    )
    def patch(self, request, pk, format=None):
        community = self.get_object(pk)
        community_serializer = CommunitySerializer(community,
                                                   data=request.data,
                                                   partial=True)
        if community_serializer.is_valid():
            community_serializer.save()
            return Response(community_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'response': 'error',
            'message': community_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="보호소에서 커뮤니티 포스트를 지우는 API입니다.",
        responses={204: None}
    )
    def delete(self, request, pk, format=None):
        community = self.get_object(pk)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
