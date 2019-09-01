from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from .models import Post,Vote
from .serializers import PostSerializer,VoteSerializer
from rest_framework import status


# Create your views here.

def index(request):
    return render(request,"garbage_app/home.html")
def base_page(request):
    return render(request,"garbage_app/base.html")


class PostList(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

class PostDetail(generics.RetrieveDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

class CreateVote(APIView):
    serializer_class=VoteSerializer
    def post(self,request,pk):
        voted_by=request.data.get("voted_by")
        data={"post":pk,"voted_by":voted_by}
        serializer=VoteSerializer(data=data)
        if serializer.is_valid():
            vote=serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)