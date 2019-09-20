"""garbage_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from garbage_app import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
# from garbage_app.views import checkpoint_view,driver_checkpoint_view,checkpoint_dustbin_view

urlpatterns = [
    path('home/',views.index,name="home"),
    path('', include('garbage_app.urls')),
    path('base/',views.base_page,name="base"),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path("postAPI/",views.PostList.as_view(),name="post_listAPI"),
    path("Garbage_UserAPI/",views.Garbage_UserList.as_view(),name="Garbage_UserListAPI"),
    path("postAPI/<int:pk>/",views.PostDetail.as_view(),name="post_details"),
    path("postAPI/<int:pk>/vote/",views.CreateVote.as_view(),name="create_vote"),
    path("user/login/",views.Login_User.as_view(),name="Login_User"),
    path("checkpointAPI/",views.checkpoint_view.as_view(),name="checkpointAPI"),
    path("driver_checkpointAPI/",views.driver_checkpoint_view.as_view(),name="driver_checkpointAPI"),
    path("checkpoint_dustbinAPI/",views.checkpoint_dustbin_view.as_view(),name="driver_checkpoint_dustbinAPI")

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


