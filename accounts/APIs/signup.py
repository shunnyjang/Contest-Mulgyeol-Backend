from datetime import timedelta

from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import User

from accounts.APIs.serializer_for_schema import CheckIdRequestSerializer
from accounts.models import PhoneAuth
from accounts.serializers import UserSerializer, PhoneAuthSerializer


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success",
                "message": "회원가입에 성공했습니다."
            }, status=status.HTTP_201_CREATED)
        return Response({
            "response": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CheckIdView(APIView):
    @extend_schema(
        parameters=[CheckIdRequestSerializer],
        responses={200: None,
                   400: None}
    )
    def get(self, request, format=None):
        try:
            user_input_id = request.query_params['id']
            exit_id_user = User.objects.get(userID=user_input_id)
            if exit_id_user:
                return Response({"result": "False"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"result": "True"}, status=status.HTTP_200_OK)


def check_auth_number(p_num, c_num):
    time_limit = now() - timedelta(minutes=5)
    try:
        result = PhoneAuth.objects.filter(
            phone_number=p_num,
            auth_number=c_num,
            modified__gte=time_limit)
        if result:
            return True
        else:
            return False
    except PhoneAuth.DoesNotExist:
        return False


class PhoneAuthView(APIView):
    @extend_schema(
        parameters=[PhoneAuthSerializer],
        responses={200: None,
                   400: None},
    )
    def get(self, request):
        try:
            p_num = request.query_params['phone_number']
            a_num = request.query_params['auth_number']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = check_auth_number(p_num, a_num)
            if result:
                return Response({'message': 'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Fail'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=PhoneAuthSerializer,
        responses={200: None,
                   400: None}
    )
    def post(self, request):
        try:
            p_num = request.data['phone_number']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            PhoneAuth.objects.update_or_create(phone_number=p_num)
            return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)
