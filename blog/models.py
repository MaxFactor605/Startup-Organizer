from django.db import models
from organizer.models import Tag, Startup
from django.urls import reverse
from django.conf import settings
from datetime import date


class PostQueryset(models.QuerySet):
    def published(self):
        return self.filter(pub_date__lte=date.today())


class PostManager(models.Manager):
    def get_by_natural_key(self, pub_date, slug):
        return self.get(pub_date=pub_date, slug=slug)

    def get_queryset(self):
        return (PostQueryset(self.model, using=self._db, hints=self._hints).select_related('author__profile')
                .prefetch_related('tags').prefetch_related('startups'))

    def published(self):
        return self.get_queryset().published()


class Post(models.Model):
    title = models.CharField(max_length=50, help_text='Give your post a title')
    slug = models.SlugField(max_length=30, help_text='A label for URL config', unique_for_month='pub_date')
    text = models.TextField(help_text='Write some of your thoughts')
    pub_date = models.DateField(verbose_name='Date published', help_text='Publication date', auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')
    startups = models.ManyToManyField(Startup, blank=True, related_name='blog_posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts', on_delete=models.CASCADE)
    objects = PostManager()

    def __str__(self):
        return '{0} on {1}'.format(self.title, self.pub_date)

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'year': self.pub_date.year,
                                                   'month': self.pub_date.month, 'slug': self.slug})

    def get_update_url(self):
        return reverse('blog_post_update', kwargs={'year': self.pub_date.year,
                                               'month': self.pub_date.month, 'slug': self.slug})

    def formatted_title(self):
        return self.title.title()

    def short_text(self):
        if len(self.text) > 20:
            short = ' '.join(self.text.split()[:20])
            short += ' ...'
        else:
            short = self.text
        return short
    
    def get_archive_year_url(self):
        return reverse('blog_post_archive_year', kwargs={'year': self.pub_date.year})

    def get_delete_url(self):
        return reverse('blog_post_delete', kwargs={'year': self.pub_date.year,
                                                   'month': self.pub_date.month, 'slug': self.slug})

    def natural_key(self):
        return(self.pub_date, self.slug)
    natural_key.dependencies = [
        'organizer.startup',
        'organizer.tag',
        'user.user',
    ]
    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'
        index_together = (('slug', 'pub_date'),)



