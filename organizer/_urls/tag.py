from organizer.views import tag_detail, tag_list, TagDelete, TagUpdate, TagCreate
from django.urls import path, re_path

urlpatterns = [
    re_path(r'(?P<slug>[\w\-]+)/update/$', TagUpdate.as_view(), name='organizer_tag_update'),
    re_path(r'(?P<slug>[\w\-]+)/delete/$', TagDelete.as_view(), name='organizer_tag_delete'),
    path('create', TagCreate.as_view(), name='organizer_tag_create'),
    re_path(r'(?P<slug>[\w\-]+)/$', tag_detail, name='organizer_tag_detail'),
    re_path(r'', tag_list, name='organizer_tag_list'),
]