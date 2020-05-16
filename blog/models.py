from django.db import models
from organizer.models import Tag, Startup
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=50, help_text='Give your post a title')
    slug = models.SlugField(max_length=30, help_text='A label for URL config', unique_for_month='pub_date')
    text = models.TextField(help_text='Write some of your thoughts')
    pub_date = models.DateField(verbose_name='Date published', help_text='Publication date', auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')
    startups = models.ManyToManyField(Startup, blank=True, related_name='blog_posts')

    def __str__(self):
        return '{0} on {1}'.format(self.title, self.pub_date)

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'year': self.pub_date.year,
                                                   'month': self.pub_date.month, 'slug': self.slug})

    def get_update_url(self):
        return reverse('blog_post_update', kwargs={'year': self.pub_date.year,
                                                   'month': self.pub_date.month, 'slug': self.slug})

    def get_delete_url(self):
        return reverse('blog_post_delete', kwargs={'year': self.pub_date.year,
                                                   'month': self.pub_date.month, 'slug': self.slug})
    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'
