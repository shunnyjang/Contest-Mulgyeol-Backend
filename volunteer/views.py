from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter

from config.permissions import IsAuthShelter, IsAuthShelterOrReadOnly, IsOwnShelterOrReadOnly
from accounts.models import User, Shelter
from volunteer.models import Post, Tag, Volunteer, UserVolunteer
from volunteer.serializers import PostSerializer, VolunteerSerializer, UserVolunteerSerializer

from django.contrib.auth import get_user_model
from django.http import Http404

class PostView(ListAPIView):

    permssion_classes = [IsAuthShelterOrReadOnly]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['tag__name']

    def get_queryset(self):
        return Post.objects.all()

    def post(self, request, format=None):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
    
        # multipart/form-parser은 QueryDict이므로 immutable 함
        # 따라서 일시적으로 mutable하게 해줌
        request.data._mutable = True
        request.data['shelter'] = request.user.shelter.pk
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
            
            # Create new volunteer objects
            days = request.data.get('term').split(',')
            for day in days:
                if not day:
                    continue
                else:
                    day = day.strip()
                    volunteer = Volunteer.objects.get_or_create(
                        shelter=request.user.shelter,
                        date=day,
                        limit_of_volunteer=request.data.get('limit'))
            return Response({ # 포스트 업로드 & 태그 등록 완료
                "response": "success",
                "message": "성공적으로 봉사모집을 업로드했습니다."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "response": "error",
                "message": serializer.errors
            })


class PostDetailView(APIView):
    
    permission_classes = [IsOwnShelterOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        
        if request.data.get('tags'):
            tags = post.tag.all()
            tags.delete()
            tags = request.data.get('tags').split(',')
            for tag in tags:
                if not tag: 
                    continue
                else:
                    tag = tag.strip()
                    tag_, created = Tag.objects.get_or_create(name=tag)
                    post.tag.add(tag_)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class VolunteerRetrieveView(APIView):

    permission_classes = [IsAuthShelter]

    def get(self, request, format=None):
        volunteer = UserVolunteer.objects.filter(volunteer__shelter=request.user.shelter.pk)
        serializer = UserVolunteerSerializer(volunteer, many=True)
        return Response(serializer.data)


class VolunteerApplyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        volunteer = Volunteer.objects.get(shelter=data.get('shelter'), date=data.get('date'))
        data['user'] = request.user.pk
        data['volunteer'] = volunteer.id
        serializer = UserVolunteerSerializer(data=data)

        volunteer.num_of_volunteer += 1
        if volunteer.num_of_volunteer <= volunteer.limit_of_volunteer:
            volunteer.save()
        else:
            return Response({
                "response": "error",
                "message": "하루 봉사 인원 정원 초과, 관리자에게 직접 문의 바람"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

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
