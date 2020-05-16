from ._urls import startup, tag, newslink
from django.urls import re_path
from django.conf.urls import include

urlpatterns=[
    re_path(r'startup', include(startup)),
    re_path(r'tag', include(tag)),
    re_path(r'^newslink', include(newslink)),
]