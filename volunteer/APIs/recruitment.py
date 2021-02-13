from django.contrib.auth import get_user_model
from django.http import Http404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwnShelterOrReadOnly
from volunteer.APIs.serializer_for_schema import RecruitmentSearchSerializer, JWTTokenScheme, \
    RecruitmentPostRequestSerializer
from volunteer.models import Recruitment
from volunteer.serializers import RecruitmentSerializer
from volunteer.utils import update_tag


class RecruitmentView(APIView):
    permission_classes = [IsOwnShelterOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        description="전국의 보호소들이 올린 자원봉사자 모집 공고를 확인할 수 있는 API입니다. parameter로 검색하고자 하는 tag들을 보내 검색할 수 있습니다.",
        parameters=[RecruitmentSearchSerializer],
        responses=RecruitmentSerializer,
    )
    def get(self, request):
        search_tags = request.GET.getlist('tags', [])
        tag_filter_recruitments = {}
        for i in range(0, search_tags.count()):
            tag_filter_recruitments[i] = search_tags[i]
        recruitment_serializer = RecruitmentSerializer(**tag_filter_recruitments, many=True)
        return Response(recruitment_serializer.data)

    @extend_schema(
        description="보호소들이 자원 봉사자 모집 공고를 올릴 수 있는 API입니다.",
        request=RecruitmentPostRequestSerializer,
        responses={201: None,
                   400: None}
    )
    def post(self, request):
        user = get_user_model().objects.get(pk=request.user.pk)

        # multipart/form-parser은 QueryDict이므로 immutable 함
        # 따라서 일시적으로 mutable하게 해줌
        request.data._mutable = True
        request.data['shelter'] = user.shelter.pk
        request.data._mutable = False

        recruitment_serializer = RecruitmentSerializer(data=request.data)
        if not recruitment_serializer.is_valid():
            return Response({
                "response": "error",
                "message": recruitment_serializer.errors
            }, status=status.HTTP_401_UNAUTHORIZED)
        recruitment_serializer.save()  # 봉사 모집 포스트 업로드 완료

        update_tag(request.data.get('tags'), recruitment_serializer.Meta.model)
        return Response({  # 포스트 업로드 & 태그 등록 완료
            "response": "success",
            "message": "성공적으로 봉사모집을 업로드했습니다."
        }, status=status.HTTP_201_CREATED)


class RecruitmentDetailView(APIView):
    permission_classes = [IsOwnShelterOrReadOnly]

    def get_object(self, pk):
        try:
            return Recruitment.objects.get(pk=pk)
        except:
            raise Http404

    @extend_schema(
        description="보호소에서 올린 봉사 모집 공고를 하나씩 보는 API입니다. 주소의 가장 마지막에 붙이는 숫자가 id인 모집 공고를 볼 수 있습니다.",
        responses=RecruitmentSerializer
    )
    def get(self, request, pk, format=None):
        recruitment = self.get_object(pk)
        recruitment_serializer = RecruitmentSerializer(recruitment)
        return Response(recruitment_serializer.data)

    @extend_schema(
        description="해당 모집 공고를 부분적으로 수정할 수 있는 API입니다. 수정하고자 하는 일부 field를 request에 포함하면 됩니다.",
        request=RecruitmentPostRequestSerializer
    )
    def patch(self, request, pk, format=None):
        recruitment = self.get_object(pk)

        # 태그 수정시 모두 삭제하고 재등록
        if request.data.get('tags'):
            tags = recruitment.tag.all()
            tags.delete()
            update_tag(request.data.get('tags'), recruitment)

        recruitment_serializer = RecruitmentSerializer(recruitment, data=request.data, partial=True)
        if recruitment_serializer.is_valid():
            recruitment_serializer.save()
            return Response(recruitment_serializer.data, status=status.HTTP_201_CREATED)
