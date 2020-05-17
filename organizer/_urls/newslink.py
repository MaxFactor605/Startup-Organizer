from organizer.views import NewslinkDelete, NewsLinkCreate, NewsLinkUpdate
from django.urls import path, re_path

urlpatterns = [
    path('create', NewsLinkCreate.as_view(), name='organizer_newslink_create'),
    re_path(r'update/(?P<pk>\d+)/$', NewsLinkUpdate.as_view(), name='organizer_newslink_update'),
    re_path(r'delete/(?P<pk>\d+)/$', NewslinkDelete.as_view(), name='organizer_newslink_delete'),
]
