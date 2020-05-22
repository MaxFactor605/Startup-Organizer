from organizer.views import StartupDetail, StartupList, StartupCreate, StartupUpdate, StartupDelete
from django.urls import path, re_path

urlpatterns = [
    path('<slug>/delete/', StartupDelete.as_view(), name='organizer_startup_delete'),
    path('<slug>/update/', StartupUpdate.as_view(), name='organizer_startup_update'),
    path('create', StartupCreate.as_view(), name='organizer_startup_create'),
    path('<slug>/', StartupDetail.as_view(), name='organizer_startup_detail'),
    path('', StartupList.as_view(), name='organizer_startup_list'),
]
