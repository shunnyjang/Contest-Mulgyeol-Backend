from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.models import User, Shelter
from volunteer.models import Post, Tag, Volunteer, UserVolunteer
from volunteer.serializers import PostSerializer, VolunteerSerializer, UserVolunteerSerializer

from django.contrib.auth import get_user_model

class PostView(APIView):

    permission_classes = [AllowAny]
    #IsAuthenticatedOrReadOnly,
    parser_classes = (FormParser, MultiPartParser,)

    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        try:
            shelter = Shelter.objects.get(user=user).id
        except:
            return Response({
                "response": "error",
                "message": "보호소 담당자가 아닙니다."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        request.data['shelter'] = shelter
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success",
                "message": "성공적으로 봉사모집을 업로드했습니다."
            })
        else:
            return Response({
                "response": "error",
                "message": serializer.errors
            })

class VolunteerView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    #IsAuthenticated, 

    def get(self, request, format=None):
        volunteer = Volunteer.objects.filter(shelter=request.data.get('shelter'))
        serializer = VolunteerSerializer(volunteer, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        volunteer = Volunteer.objects.get(shelter=data['shelter'], date=data['date'])
        data['num_of_volunteer'] = volunteer.num_ov_volunteer + 1
        serializer = VolunteerSerializer(data=data)

        uvSerializer = UserVolunteerSerializer(data={
            "user": request.user.pk,
            "volunteer": serializer.data.get('id')
        })

        if uvSerializer.is_valid():
            uvSerializer.save()
        else:
            return Response({
                "response": "error",
                "message": uvSerializer.errors
            })

        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success",
                "message": "봉사신청이 완료되었습니다."
            })
        else:
            return Response({
                "response": "error",
                "message": serializer.errors
            })
