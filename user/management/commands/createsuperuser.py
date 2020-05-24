from .createuser import Command as BaseCommand
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from ...models import Profile
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Create Super User'

    def create_user(self, username, email, password):
        new_user = self.User.objects.create_superuser(username, email,  password)

        try:
            Profile.objects.create(user=new_user, slug=slugify(username))
        except Exception as e:
            raise CommandError('Could not create a Profile:\n'.format('; '.join(e.messages)))


