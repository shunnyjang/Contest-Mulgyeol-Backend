from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import ObtainJSONWebToken
from accounts.serializers import UserSerializer, ShelterSerializer
from accounts.models import User, PhoneAuth, Shelter

from django.utils.timezone import now
from datetime import timedelta

from django.http import Http404
from django.contrib.auth import get_user_model

class LoginTestView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            User = get_user_model()
            user = User.objects.get(pk=request.user.pk)

            if user:
                return Response({
                    "response": "success"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "response": "error"
                }, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({
                    "response": "error"
                }, status=status.HTTP_401_UNAUTHORIZED)
                
class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success",
                "message": "회원가입에 성공했습니다."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "resopnse": "error",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class CheckIdView(APIView):
    def get(self, request, format=None):
        try:
            id = request.query_params['id']
            user = User.objects.get(userID=id)
            if user:
                return Response({"result": "False"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"result": "True"}, status=status.HTTP_200_OK) 


class ShelterCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data.get('profile'))
        shelter = ShelterSerializer(data=request.data.get('shelter'))
        if user.is_valid():
            user.save()
            if shelter.is_valid():
                shelter.save()
                return Response({
                    "response": "success",
                    "message": "성공적으로 보호소를 등록했습니다."
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                "resopnse": "error",
                "message": shelter.errors
            }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({
                "resopnse": "error",
                "message": user.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class ShelterDetailView(APIView):
    def get_object(self, pk):
        try:
            return Shelter.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        shelter = self.get_object(pk)
        serializer = ShelterSerializer(shelter)
        return Response(serializer.data)
            
    
    def patch(self, request, pk, format=None):
        shelter = self.get_object(pk)
        serializer = ShelterSerializer(shelter, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success", 
                "message": "성공적으로 수정하였습니다."})
        return Response({
            "response": "error", 
            "message" : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


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

    def post(self, request):
        try:
            p_num = request.data['phone_number']
        except KeyError:
            return Response({
                'message': 'Bad Request'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            PhoneAuth.objects.update_or_create(phone_number=p_num)
            return Response({'message': 'OK'})

class LoginJWTView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, content_type='application/json')

        if response.status_code != 200:
            return Response({
                'response': 'error',
                'message': '로그인이 실패하였습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        userID = request.data.get('userID')
        try:
            user = User.objects.get(userID=userID)
        except User.DoesNotExist:
            return Response({
                'response': 'error',
            }, status=status.HTTP_400_BAD_REQUEST)

        update_last_login(None, user)
        return Response({
            'response': 'success',
            'token': response.data['token']
            }, status=status.HTTP_200_OK)
