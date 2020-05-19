from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from organizer import urls as organizer_urls
from blog import urls as blog_urls
from contact import urls as contact_urls
from django.contrib.flatpages import urls as flatpages_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include(organizer_urls)),
    re_path(r'^', include(blog_urls)),
    re_path(r'^', include(contact_urls)),
    re_path(r'^', include(flatpages_urls)),
]
