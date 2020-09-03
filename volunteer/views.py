from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from config.permissions import IsAuthShelter, IsAuthShelterOrReadOnly
from accounts.models import User, Shelter
from volunteer.models import Post, Tag, Volunteer, UserVolunteer
from volunteer.serializers import PostSerializer, VolunteerSerializer, UserVolunteerSerializer

from django.contrib.auth import get_user_model

class PostView(APIView):

    permission_classes = [IsAuthShelterOrReadOnly]
    parser_classes = (FormParser, MultiPartParser,)

    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        
        # request.user의 보호소 찾기
        try:
            shelter = Shelter.objects.get(user=user).id
        except Shelter.DoesNotExist:
            return Response({
                "response": "error",
                "message": "보호소 담당자가 아닙니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # multipart/form-parser은 QueryDict이므로 immutable 함
        # 따라서 일시적으로 mutable하게 해줌
        request.data._mutable = True
        request.data['shelter'] = shelter
        request.data._mutable = False

        # Create a new post object
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # 봉사 모집 포스트 업로드 완료
            # Create new tag objects
            tags = request.data.get('tags').split(',')
            for tag in tags:
                if not tag: 
                    continue
                else:
                    tag = tag.strip()
                    tag_, created = Tag.objects.get_or_create(name=tag)
                    serializer.instance.tag.add(tag_)
            return Response({ # 포스트 업로드 & 태그 등록 완료
                "response": "success",
                "message": "성공적으로 봉사모집을 업로드했습니다."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "response": "error",
                "message": serializer.errors
            })


class VolunteerView(APIView):

    permission_classes = [IsAuthShelter]

    def get(self, request, format=None):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        
        # request.user의 보호소 찾기
        try:
            shelter = Shelter.objects.get(user=user).id
        except Shelter.DoesNotExist:
            return Response({
                "response": "error",
                "message": "보호소 담당자가 아닙니다."
            }, status=status.HTTP_400_BAD_REQUEST)

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
