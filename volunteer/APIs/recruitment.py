from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import Http404
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.APIs.serializer_for_schema import ApiResponseSerializer
from config.permissions import IsAuthShelterOrReadOnly
from volunteer.APIs.serializer_for_schema import RecruitmentSearchSerializer, RecruitmentPostRequestSerializer, \
    DailyRecruitmentPostRequestSerializer, DailyRecruitmentPostResponeSerializer, \
    DailyRecruitmentDetailRequestSerializer, RecruitmentResponseSerializer
from volunteer.models import Recruitment, DailyRecruitmentStatus
from volunteer.serializers import RecruitmentSerializer, DailyRecruitmentStatusSerializer
from volunteer.utils import update_tag, save_daily_recruitment_objects


class RecruitmentView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        description="""
        전국의 보호소들이 올린 자원봉사자 모집 공고를 확인할 수 있는 API입니다. 
        parameter로 검색하고자 하는 tag들을 보내 검색할 수 있습니다.
        tag는 여러 개 중첩 사용가능합니다. (OR로 검색 결과 반환)
        """,
        parameters=[RecruitmentSearchSerializer],
        responses=RecruitmentResponseSerializer,
    )
    def get(self, request):
        search_tags = request.GET.getlist('tag', [])
        search_locations = request.GET.getlist('location', [])

        if search_locations:
            query = Q()
            for search_location in search_locations:
                query = query | Q(shelter__loc_short__startswith=search_location)
            recruitment = Recruitment.objects.filter(query)
        else:
            recruitment = Recruitment.objects.all()

        if search_tags:
            recruitment = recruitment.filter(tags__text__in=search_tags)

        recruitment_serializer = RecruitmentSerializer(recruitment, many=True)
        return Response(recruitment_serializer.data)

    @extend_schema(
        description="보호소들이 자원 봉사자 모집 공고를 올릴 수 있는 API입니다.",
        request=RecruitmentPostRequestSerializer,
        responses={201: ApiResponseSerializer,
                   400: ApiResponseSerializer}
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
        recruitment_object = recruitment_serializer.save()  # 봉사 모집 포스트 업로드 완료

        update_tag(request.data.get('tags'), recruitment_object)
        save_daily_recruitment_objects(user.shelter,
                                       request.data.get('start_date'),
                                       request.data.get('end_date'))
        return Response({  # 포스트 업로드 & 태그 등록 완료
            "response": "success",
            "message": "성공적으로 봉사모집을 업로드했습니다."
        }, status=status.HTTP_201_CREATED)


class RecruitmentDetailView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]

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
        request=RecruitmentPostRequestSerializer,
        responses={200: RecruitmentSerializer,
                   400: ApiResponseSerializer}
    )
    def patch(self, request, pk, format=None):
        recruitment = self.get_object(pk)

        # 태그 수정시 모두 삭제하고 재등록
        if request.data.get('tags'):
            recruitment.tags.clear()
            update_tag(request.data.get('tags'), recruitment)

        save_daily_recruitment_objects(request.user.shelter,
                                       request.data.get('start_date'),
                                       request.data.get('end_date'))

        recruitment_serializer = RecruitmentSerializer(recruitment, data=request.data, partial=True)
        if recruitment_serializer.is_valid():
            recruitment_serializer.save()
            return Response(recruitment_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'response': 'error',
            'message': recruitment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DailyRecruitmentDetailView(APIView):
    permission_classes = [IsAuthShelterOrReadOnly]

    def get_object(self, pk):
        try:
            return DailyRecruitmentStatus.objects.get(pk=pk)
        except:
            raise Http404

    @extend_schema(
        description="보호소에서 올린 봉사 모집 공고를 하나씩 보는 API입니다. 주소의 가장 마지막에 붙이는 숫자가 id인 모집 공고를 볼 수 있습니다.",
        responses=DailyRecruitmentStatusSerializer
    )
    def get(self, request, pk, format=None):
        daily_recruitment = self.get_object(pk)
        daily_recruitment_serializer = DailyRecruitmentStatusSerializer(daily_recruitment)
        return Response(daily_recruitment_serializer.data)

    @extend_schema(
        description="해당 모집 공고를 부분적으로 수정할 수 있는 API입니다. 그 날 필요한 인원수를 수정할 수 있습니다.",
        request=DailyRecruitmentDetailRequestSerializer,
        responses={200: DailyRecruitmentStatusSerializer,
                   400: ApiResponseSerializer}
    )
    def patch(self, request, pk, format=None):
        daily_recruitment = self.get_object(pk)
        daily_recruitment_serializer = DailyRecruitmentStatusSerializer(daily_recruitment,
                                                                        data=request.data,
                                                                        partial=True)
        if daily_recruitment_serializer.is_valid():
            daily_recruitment_serializer.save()
            return Response(daily_recruitment_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'response': 'error',
            'message': daily_recruitment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="보호소에서 올렸던 봉사 모집 날짜를 지우는 API입니다.",
        responses={204: None}
    )
    def delete(self, request, pk, format=None):
        daily_recruitment = self.get_object(pk)
        daily_recruitment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
