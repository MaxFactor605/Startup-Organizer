from datetime import date
from django.contrib.sitemaps import Sitemap
from .models import Post
from math import log10

class PostSitemap(Sitemap):
    changefreq = 'never'

    def items(self):
        return Post.objects.all()

    def lastmod(self, post):
        return post.pub_date

    def priority(self, post):
        period = 90
        timedelta = date.today() - post.pub_date
        days = timedelta.total_seconds()

        if days == 0:
            return 1.0
        elif 0 < days <=period:
            normalized = (log10(period/days)/log10(period**2))
            normalized = round(normalized, 2)
            return normalized + 0.5
        else:
            return 0.5
