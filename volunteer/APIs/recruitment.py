from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwnShelterOrReadOnly
from volunteer.models import Recruitment
from volunteer.serializers import RecruitmentSerializer
from volunteer.utils import update_tag


class RecruitmentView(APIView):
    permission_classes = [IsOwnShelterOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        search_tags = request.GET.getlist('search_tags', [])
        tag_filter_recruitments = {}
        for i in range(0, search_tags.count()):
            tag_filter_recruitments[i] = search_tags[i]
        recruitment_serializer = RecruitmentSerializer(**tag_filter_recruitments, many=True)
        return Response(recruitment_serializer.data)

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

    def get(self, request, pk, format=None):
        recruitment = self.get_object(pk)
        recruitment_serializer = RecruitmentSerializer(recruitment)
        return Response(recruitment_serializer.data)

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
