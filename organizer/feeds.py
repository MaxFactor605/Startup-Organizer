from datetime import datetime

from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from .models import Startup

class BaseStartupFeedMixin:
    def get_object(self, request, startup_slug):
        return get_object_or_404(Startup, slug__iexact=startup_slug)

    def description(self, startup):
        return 'News related to {0}'.format(startup.name)

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link_to_article

    def item_title(self, item):
        return item.title

    def items(self, startup):
        return startup.newslink_set.all()[:10]

    def link(self, startup):
        return startup.get_absolute_url()

    def subtitle(self, startup):
        return self.description(startup)

    def title(self, startup):
        return startup.name


class AtomStartupFeed(BaseStartupFeedMixin, Feed):
    feed_type = Atom1Feed

class Rss2StartupFeed(BaseStartupFeedMixin, Feed):
    feed_type = Rss201rev2Feed



