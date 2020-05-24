# Generated by Django 3.1 on 2020-05-24 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizer', '0007_auto_20200522_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='startups', to='auth.user'),
            preserve_default=False,
        ),
    ]
