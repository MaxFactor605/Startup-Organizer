from django.conf.urls import include
from user import urls as auth_urls
from django.contrib import admin
from django.urls import path, re_path
from organizer import urls as organizer_urls
from blog import urls as blog_urls
from contact import urls as contact_urls
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include(organizer_urls)),
    re_path(r'^', include(blog_urls)),
    re_path(r'^', include(contact_urls)),
    path('about/', TemplateView.as_view(template_name='site/about.html'), name='about_site'),
    path('', RedirectView.as_view(pattern_name='blog_post_list', permanent=False)),
    path('user/', include(auth_urls))
]
