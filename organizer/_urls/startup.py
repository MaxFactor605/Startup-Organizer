from organizer.views import startup_detail, StartupList, StartupCreate, StartupUpdate, StartupDelete
from django.urls import path, re_path

urlpatterns = [
    re_path(r'(?P<slug>[\w\-]+)/delete/$', StartupDelete.as_view(), name='organizer_startup_delete'),
    re_path(r'(?P<slug>[\w\-]+)/update/$', StartupUpdate.as_view(), name='organizer_startup_update'),
    path('create', StartupCreate.as_view(), name='organizer_startup_create'),
    re_path(r'(?P<slug>[\w\-]+)/$', startup_detail, name='organizer_startup_detail'),
    path('/', StartupList.as_view(), name='organizer_startup_list'),
]
