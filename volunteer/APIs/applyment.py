from calendar import calendar
from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Shelter
from volunteer.models import DailyRecruitmentStatus, Volunteer
from volunteer.serializers import DailyRecruitmentStatusSerializer, VolunteerSerializer


class VolunteerApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        봉사 가능 날짜 확인 (이번 달)
        """
        today = date.today()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        last_day_of_the_month = date(today.year, today.month, last_day_of_the_month)

        volunteer_recruitment_calendar = DailyRecruitmentStatus.objects.filter(
            shelter=request.query_params['shelter'], date__gt=today, date__lte=last_day_of_the_month)
        recruitment_status_serializer = DailyRecruitmentStatusSerializer(volunteer_recruitment_calendar, many=True)
        return Response(recruitment_status_serializer.data)

    def post(self, request, format=None):
        """
        봉사 신청
        """
        user = get_user_model().objects.get(pk=request.user.pk)
        applying_for = DailyRecruitmentStatus.objects.get(
            shelter=request.data.get('shelter'), date=request.data.get('date'))
        applying_for.current_number += 1
        if applying_for.current_number <= applying_for.need_number:
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
            })
        return Response({
            "response": "error",
            "message": volunteer_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view('GET')
@permission_classes([IsAuthenticated])
def list_of_applying_volunteer_of_user(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    user_applying_volunteer_list = Volunteer.objects.filter(user=user)
    volunteer_serializer = VolunteerSerializer(user_applying_volunteer_list, many=True)
    return Response(volunteer_serializer.data)


@api_view('GET')
@permission_classes([IsAuthenticated])
def list_of_volunteer_for_shelter(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    shelter = Shelter.objects.get(user=user)
    list_of_volunteer = Volunteer.objects.filter(applying_for__shelter=shelter)
    volunteer_serializer = VolunteerSerializer(list_of_volunteer, many=True)
    return Response(volunteer_serializer.data)
