from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView, TemplateView
from django.conf.urls import include
from django.urls import reverse_lazy
from .views import ProfileUpdate, PublicProfileDetail, ProfileDetail, DisableAccount, ActivateAccount, CreateAccount, ResendActivationEmail


password_urls = [
    path('', RedirectView.as_view(pattern_name='user_pw_reset_start', permanent=False)),
    path('change/', auth_views.PasswordChangeView.as_view(template_name='user/pw_change_form.html',
                                                          success_url=reverse_lazy('user_pw_change_done')),
                                                          name='user_pw_change'),
    path('change/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/pw_change_done.html'),
                                                                  name='user_pw_change_done'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='user/pw_reset_form.html',
                                                        email_template_name='user/pw_reset_email.html',
                                                        subject_template_name='user/pw_reset_subject.html',
                                                        success_url=reverse_lazy('user_pw_reset_sent')),
                                                        name='user_pw_reset_start'),
    path('reset/sent/', auth_views.PasswordResetDoneView.as_view(template_name='user/pw_reset_sent.html'),
                                                                name='user_pw_reset_sent'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/pw_reset_confirm.html',
                                                                post_reset_login=reverse_lazy('user_pw_reset_complete')),
                                                                name='user_pw_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/pw_reset_complete.html',
                                                                 extra_context={'form': AuthenticationForm}),
                                                                 name='user_pw_reset_complete'),

]
urlpatterns=[
    path('', RedirectView.as_view(pattern_name='user_login', permanent=False)),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user_login'),
    path('logout/', auth_views.logout_then_login, name='user_logout'),
    path('password/', include(password_urls)),
    path('disable/', DisableAccount.as_view(), name='user_disable'),
    path('create/', CreateAccount.as_view(), name='user_create'),
    path('activate', RedirectView.as_view(pattern_name='user_activate_resend', permanent=False)),
    path('create/done', TemplateView.as_view(template_name='user/user_create_done.html'), name='user_create_done'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='user_activate'),
    path('activate/resend/', ResendActivationEmail.as_view(), name='user_activate_resend'),
    path('profile/', ProfileDetail.as_view(), name='user_profile'),
    path('profile/edit/', ProfileUpdate.as_view(), name='user_profile_update'),
    path('profile/<slug>/', PublicProfileDetail.as_view(), name='user_pub_profile'),
]