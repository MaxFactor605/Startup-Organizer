from django.conf.urls import include
from user import urls as auth_urls
from django.contrib import admin
from django.urls import path, re_path
from organizer import urls as organizer_urls
from blog import urls as blog_urls
from contact import urls as contact_urls
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.urls import include, path
from blog.feeds import AtomPostFeed, Rss2PostFeed
from django.contrib.sitemaps.views import index as site_index_view, sitemap as sitemap_view
from .sitemaps import sitemaps as sitemaps_dict


sitenews = [
    path('atom/', AtomPostFeed(), name='blog_atom_feed'),
    path('rss/', Rss2PostFeed(), name='blog_rss_feed'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include(organizer_urls)),
    re_path(r'^', include(blog_urls)),
    re_path(r'^', include(contact_urls)),
    path('about/', TemplateView.as_view(template_name='site/about.html'), name='about_site'),
    path('', RedirectView.as_view(pattern_name='blog_post_list', permanent=False)),
    path('user/', include(auth_urls)),
    path('sitenews/', include(sitenews)),
    re_path(r'^sitemap\.xml$', site_index_view, {'sitemaps': sitemaps_dict}, name='sitemap'),
    re_path(r'^sitemap-(?P<section>.+)\.xml$', sitemap_view, {'sitemaps': sitemaps_dict}, name='sitemaps_sections'),

]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

