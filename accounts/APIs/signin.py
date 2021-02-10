from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from accounts.models import User


class LoginTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"response": "login success"}, status=status.HTTP_200_OK)


class LoginJWTView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, content_type='application/json')

        if response.status_code != 200:
            return Response({
                'response': 'error',
                'message': '로그인이 실패하였습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('userID')
        try:
            user = User.objects.get(userID=user_id)
        except User.DoesNotExist:
            return Response({
                'response': 'error',
            }, status=status.HTTP_400_BAD_REQUEST)

        update_last_login(None, user)
        return Response({
            'response': 'success',
            'token': response.data['token']
        }, status=status.HTTP_200_OK)
