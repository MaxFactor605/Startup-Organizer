from django.db import models
from django.urls import reverse
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='Tag name')
    slug = models.SlugField(max_length=30, unique=True, help_text='A label for URL config')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizer_tag_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizer_tag_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer_tag_delete', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class Startup(models.Model):
    name = models.CharField(max_length=50, help_text='Name of company', db_index=True)
    slug = models.SlugField(max_length=30, unique=True, help_text='A label for URL config')
    description = models.TextField(help_text='Desribe your startup')
    found_date = models.DateField(verbose_name='Foundation date', help_text='When it was founded?')
    email = models.EmailField(help_text='Tell how to contact with you!')
    website = models.URLField(max_length=255, help_text='Your best startup website')
    tags = models.ManyToManyField(Tag, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='startups', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizer_startup_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizer_startup_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer_startup_delete', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        get_latest_by = 'found_date'



class NewsLink(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    link_to_article = models.URLField(max_length=255)
    pub_date = models.DateField(verbose_name='Date published', auto_now_add=True)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} : {1}'.format(self.startup, self.title)

    class Meta:
        verbose_name = 'news article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = (('slug', 'startup'),)

    def get_absolute_url(self):
        return self.startup.get_absolute_url()

    def get_update_url(self):
        return reverse('organizer_newslink_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('organizer_newslink_delete', kwargs={'pk': self.pk})
