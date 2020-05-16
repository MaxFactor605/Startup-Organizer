from django.urls import path, re_path
from .views import post_detail, PostList, PostCreate, PostUpdate, PostDelete

urlpatterns=[
    path('post/create', PostCreate.as_view(), name='blog_post_create'),
    re_path(r'^post/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[\w\-]+)/$', post_detail,
            {'parent_template' : 'base.html'}, name='blog_post_detail'),
    re_path(r'^post/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[\w\-]+)/update/$',
            PostUpdate.as_view(), name='blog_post_update'),
    re_path(r'^post/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[\w\-]+)/delete/$',
            PostDelete.as_view(), name='blog_post_delete'),
    path('posts/', PostList.as_view(), {'parent_template' : 'base.html'}, name='blog_post_list'),
]