from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


from garbage_app.forms import CommentForm, PostForm

from .models import (Comment, Garbage_User, Post, Vote, checkpoint,
                     driver_checkpoint,checkpoint_dustbin)
from .serializers import (Garbage_UserSerializer, PostSerializer,
                          VoteSerializer, checkpoint_Serializer,
                          driver_checkpoint_Serializer,checkpoint_dustbin_Serializer)

# Create your views here.

def index(request):
    return render(request,"garbage_app/home.html")
def base_page(request):
    return render(request,"garbage_app/base.html")


class Garbage_UserList(generics.ListCreateAPIView):
    queryset=Garbage_User.objects.all()
    serializer_class=Garbage_UserSerializer

class Login_User(APIView):

    def validate_Login_User(self,request):
        if request.method==POST:
            email_from_API=request.POST("email")
            queryset=Garbage_User.objects.get(email=email_from_API)
            if (queryset):
                return Response({"error":True,"Message":"User is registered"})
            else:
                return Response({"error":False,"Message":"User is not registered"})






class PostList(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer


class checkpoint_view(generics.ListCreateAPIView):
    queryset=checkpoint.objects.all()
    serializer_class=checkpoint_Serializer



# assuming obj is your model instance




# @api_view(['GET'])
# def checkpoint_view(request, format=None):
#     """
#     A view that can accept POST requests with JSON content.
#     """
#     dict_obj = model_to_dict(checkpoint.objects.all())
#     serialized = json.dumps(dict_obj)

#     #data = serializers.serialize('json',)
#     #queryset=checkpoint.objects.all()
#     return JsonResponse(serialized,safe=False)


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




class driver_checkpoint_view(generics.ListCreateAPIView):
    queryset=driver_checkpoint.objects.all()
    serializer_class=driver_checkpoint_Serializer

class checkpoint_dustbin_view(generics.ListCreateAPIView):
    queryset=checkpoint_dustbin.objects.all()
    serializer_class=checkpoint_dustbin_Serializer
    


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




