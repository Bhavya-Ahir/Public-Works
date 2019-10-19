from django.conf.urls import url
from . import views




urlpatterns = [
    url(r'^$',views.index,name='home_page'),
    url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='user_detail'),

    url(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^post/$',views.view_all_posts,name="post_list"),
    url(r'^users/$', views.view_all_users, name="user_list"),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
]