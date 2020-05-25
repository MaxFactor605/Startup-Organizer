from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from datetime import date
from django.contrib.auth import get_user_model
UserModel = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=30, unique=True)
    about = models.TextField(blank=True)
    joined = models.DateTimeField('Date Joined', auto_now_add=True)

    def get_startups(self):
        return self.user.startups.all()

    def published_posts(self):
        return self.user.blog_posts.filter(pub_date__month=date.today().month, pub_date__year=date.today().year)

    def get_update_url(self):
        return reverse('user_profile_update')

    def get_absolute_url(self):
        return reverse('user_pub_profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.get_username()

"""
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        is_staff = kwargs.pop('is_stuff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        return self._create_user(email, password, is_staff=True, is_superuser=True, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=254, unique=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return self.profile.get_absolute_url()

    def get_full_name(self):
        return self.profile.name

    def get_short_name(self):
        return self.profile.name
"""

