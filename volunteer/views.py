from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from volunteer.models import Post, Tag, Volunteer
from volunteer.serializers import PostSerializer, VolunteerSerializer


class PostView(APIView):
    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
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