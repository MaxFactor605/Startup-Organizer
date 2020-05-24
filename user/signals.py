from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.messages import success
from django.dispatch import receiver

@receiver(user_logged_in)
def display_login_message(sender, **kwargs):
    request = kwargs.get('request')
    user = kwargs.get('user')
    success(request, 'Succesfully logged in as {0}'.format(user.username), fail_silently=True)


@receiver(user_logged_out)
def display_logout_message(sender, **kwargs):
    request = kwargs.get('request')
    success(request, 'Succesfully logged out', fail_silently=True)
