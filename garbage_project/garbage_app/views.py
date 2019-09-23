from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from .models import Post,Vote,Comment,Garbage_User
from .serializers import PostSerializer,VoteSerializer,Garbage_UserSerializer
from rest_framework import status
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from garbage_app.forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse    
import logging
logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# Create your views here.

def index(request):
    return render(request,"garbage_app/home.html")
def base_page(request):
    return render(request,"garbage_app/base.html")


class Garbage_UserList(generics.ListCreateAPIView):
    queryset=Garbage_User.objects.all()
    serializer_class=Garbage_UserSerializer

@api_view(['POST'])
@parser_classes([JSONParser])

def validate_Garbage_User_view(request):

    dict={}
    l=[]

    try:
        email_id_received=request.data[0]["email_id"]
        password_received=request.data[0]["password"]
        req_user=Garbage_User.objects.filter(email_id=email_id_received).first()
        # if Type(req_user)==None:
        #     return Response({"message":"User Not Found"})
        actual_password=req_user.password

        if actual_password==password_received:
            serializer=Garbage_UserSerializer(req_user)
            dict["error"]=False
            dict["message"]="Login Successfull"
            dict["user"]=serializer.data


            l.append(dict)
            # new_dict={**dict,**serializer.data}
            # return Response(dict)
            return JsonResponse(l,safe=False)

        else:
            dict["message"]="Incorrect Password"
            dict["error"]=True
            l.append(dict)

            return JsonResponse(l,safe=False)
            
    except :

        dict["error"]=True
        dict["message"]="User not found"
        l.append(dict)
        return JsonResponse(l,safe=False)
        
@api_view(['POST'])
def Register_Garbage_User(request):

    serializer=Garbage_UserSerializer(data=request.data)
    dict={}
    if serializer.is_valid():
        email=request.data["email_id"]
        # logging.debug(email)
        # logging.debug(Garbage_User.objects.get(email_id=email))

        try:
            if Garbage_User.objects.get(email_id=email)!=None:
                dict["error"]=True
                dict["message"]="User with same emailID already exists"
                return Response(dict)

        except Garbage_User.DoesNotExist:
                serializer.save()
                required_user=Garbage_User.objects.get(email_id=email)
                user_id=required_user.id
                dict["message"]="Succesfully registered"
                dict["error"]=False
                dict["user"]=serializer.data
                
                return Response(dict)

    return Response({"message":"registration failed"})




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


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.all()

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'garbage_app/post_detail.html'

    form_class = PostForm()

    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'garbage_app/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'garbage_app/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'garbage_app/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


