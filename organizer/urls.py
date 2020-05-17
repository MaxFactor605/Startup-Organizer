from ._urls import startup, tag, newslink
from django.urls import re_path
from django.conf.urls import include

urlpatterns=[
    re_path(r'startups', include(startup)),
    re_path(r'tags', include(tag)),
    re_path(r'newslinks', include(newslink)),
]