# Generated by Django 3.1 on 2020-05-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Give your post a title', max_length=50)),
                ('slug', models.SlugField(help_text='A label for URL config', max_length=30, unique_for_month='pub_date')),
                ('text', models.TextField(help_text='Write some of your thoughts')),
                ('pub_date', models.DateField(auto_now_add=True, help_text='Publication date', verbose_name='Date published')),
                ('startups', models.ManyToManyField(related_name='blog_posts', to='organizer.Startup')),
                ('tags', models.ManyToManyField(related_name='blog_posts', to='organizer.Tag')),
            ],
            options={
                'verbose_name': 'blog post',
                'ordering': ['-pub_date', 'title'],
                'get_latest_by': 'pub_date',
            },
        ),
    ]