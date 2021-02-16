from datetime import date, timedelta

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.APIs.serializer_for_schema import ApiResponseSerializer
from accounts.models import Shelter, User
from volunteer.APIs.serializer_for_schema import VolunteerApplyReqeustSeriazlier
from volunteer.models import DailyRecruitmentStatus, Volunteer
from volunteer.serializers import DailyRecruitmentStatusSerializer, VolunteerSerializer, \
    DailyRecruitmentVolunteerSerializer


class VolunteerApplyView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=DailyRecruitmentStatusSerializer
    )
    def get(self, request, format=None):
        """
        봉사 가능 날짜 확인 (30)
        """
        today = date.today()
        date_limit = today + timedelta(days=30)

        volunteer_recruitment_calendar = DailyRecruitmentStatus.objects.filter(
            shelter=request.query_params['shelter'], date__gt=today, date__lte=date_limit)
        recruitment_status_serializer = DailyRecruitmentStatusSerializer(volunteer_recruitment_calendar, many=True)
        return Response(recruitment_status_serializer.data)

    @extend_schema(
        request=VolunteerApplyReqeustSeriazlier,
        responses={201: ApiResponseSerializer,
                   400: ApiResponseSerializer}
    )
    def post(self, request, format=None):
        """
        봉사 신청
        """
        user = get_user_model().objects.get(pk=request.user.pk)
        try:
            applying_for = DailyRecruitmentStatus.objects.get(
                shelter=request.data.get('shelter'), date=request.data.get('date'))
        except DailyRecruitmentStatus.DoesNotExist:
            return Response({
                "response": "error",
                "message": "해당 날짜에는 보호소에서 봉사를 모집하지 않습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            if applying_for.applicant.get(pk=user.pk):
                return Response({
                    "response": "error",
                    "message": "이미 신청한 이력이 있습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        if applying_for.current_number + 1 <= applying_for.need_number:
            applying_for.current_number += 1
            applying_for.applicant.add(user)
            applying_for.save()
        else:
            return Response({
                "response": "error",
                "message": "하루 봉사 인원 정원 초과, 관리자에게 직접 문의 바람"
            }, status=status.HTTP_400_BAD_REQUEST)

        volunteer_data = {"user": user, "applying_for": applying_for}
        volunteer_serializer = VolunteerSerializer(volunteer_data)
        if volunteer_serializer.is_valid():
            volunteer_serializer.save()
            return Response({
                "response": "success",
                "message": "봉사신청이 완료되었습니다."
            }, status=status.HTTP_201_CREATED)

        return Response({
            "response": "error",
            "message": volunteer_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="사용자가 자신의 봉사신청 내역을 확인할 수 있는 API입니다.",
    responses=VolunteerSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_of_applying_volunteer_of_user(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    user_applying_volunteer_list = Volunteer.objects.filter(user=user)
    volunteer_serializer = VolunteerSerializer(user_applying_volunteer_list, many=True)
    return Response(volunteer_serializer.data)


@extend_schema(
    description="보호소가 봉사신청한 봉사자 목록을 확인할 수 있는 API입니다.",
    responses=DailyRecruitmentVolunteerSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_of_volunteer_for_shelter(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    shelter = Shelter.objects.get(user=user)
    list_of_volunteer = DailyRecruitmentStatus.objects.filter(shelter=shelter)
    volunteer_serializer = DailyRecruitmentVolunteerSerializer(list_of_volunteer, many=True)
    return Response(volunteer_serializer.data)
