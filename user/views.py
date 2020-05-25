from django.conf import settings
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout, get_user, get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .forms import UserCreationForm, ResendActivationEmailForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib.messages import error, success
from django.contrib.auth.tokens import default_token_generator as token_generator
from .utils import MailContextViewMixin, ProfileGetObjectMixin
from .models import Profile
from django.contrib.auth.models import Group
from organizer.utils import ObjectUpdateMixin

class DisableAccount(View):
	success_url = settings.LOGIN_REDIRECT_URL
	template_name = 'user/user_confirm_delete.html'

	@method_decorator(csrf_protect)
	@method_decorator(login_required)
	def get(self, request):
		return TemplateResponse(request, self.template_name)

	@method_decorator(csrf_protect)
	@method_decorator(login_required)
	def post(self, request):
		user = get_user(request)
		user.set_unusable_password()
		user.is_active = False
		user.save()
		logout(request)
		return redirect(self.success_url)


class ActivateAccount(View):
	success_url = reverse_lazy('user_login')
	template_name = 'user/user_activate.html'

	@method_decorator(never_cache)
	def get(self, request, uidb64, token):
		User = get_user_model()
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user is not None and token_generator.check_token(user, token):
			user.is_active = True
			user.groups.set([Group.objects.get(name='Average_user')])
			user.save()
			success(request, 'User activated, you may login now')
			return redirect(self.success_url)
		else:
			return TemplateResponse(request, self.template_name)


class CreateAccount(MailContextViewMixin, View):
	form_class = UserCreationForm
	success_url = reverse_lazy('user_create_done')
	template_name = 'user/user_create.html'

	@method_decorator(csrf_protect)
	def get(self, request):
		return TemplateResponse(request, self.template_name, context={'form': self.form_class()})

	@method_decorator(csrf_protect)
	@method_decorator(sensitive_post_parameters('password1', 'password2'))
	def post(self, request):
		bound_form = self.form_class(request.POST)
		if bound_form.is_valid():
			bound_form.save(**self.get_save_kwargs(request))
			if bound_form.mail_sent:
				return redirect(self.success_url)
			else:
				errs = (bound_form.non_field_errors())
				for err in errs:
					error(request, err)
					return redirect('user_activate_resend')

		return TemplateResponse(request, self.template_name, context={'form': bound_form})


class ResendActivationEmail(MailContextViewMixin, View):
	form_class = ResendActivationEmailForm
	success_url = reverse_lazy('user_login')
	template_name = 'user/resend_activation.html'

	@method_decorator(csrf_protect)
	def get(self, request):
		return TemplateResponse(request, self.template_name, {'form': self.form_class()})

	@method_decorator(csrf_protect)
	def post(self, request):
		bound_form = self.form_class(request.POST)
		if bound_form.is_valid():
			user = bound_form.save(**self.get_save_kwargs(request))
			if user is not None and not bound_form.mail_sent:
				errs = (bound_form.non_field_errors())
				for err in errs:
					error(request, err)
				if errs:
					bound_form.errors.pop('__all__')
				return TemplateResponse(request, self.template_name, {'form': bound_form})
		success(request, 'Activation Email Sent!')
		return redirect(self.success_url)


class PublicProfileDetail(View):
	model = Profile
	template_name = 'user/profile_detail.html'

	def get(self, request, slug):
		profile = get_object_or_404(self.model, slug=slug)
		return render(request, self.template_name, context={'profile': profile})


class ProfileDetail(ProfileGetObjectMixin, View):
	model = Profile
	template_name = 'user/profile_detail.html'

	@method_decorator(login_required)
	def get(self, request):
		user = self.get_object()
		profile = self.model.objects.get(user=user)
		return render(request, self.template_name, context={'profile': profile})


class ProfileUpdate(ProfileGetObjectMixin,  View):
	model = Profile
	form_class = ProfileUpdateForm
	template_name = 'user/profile_update.html'

	def get(self, request):
		user = self.get_object()
		profile = self.model.objects.get(user=user)
		return render(request, self.template_name,
					  context={'form': self.form_class(instance=profile), 'profile': profile})

	def post(self, request):
		user = self.get_object()
		profile = self.model.objects.get(user=user)
		bound_form = self.form_class(request.POST, instance=profile)
		if bound_form.is_valid():
			bound_form.save()
			return redirect('user_profile')
		else:
			return render(request, self.template_name,
						  context={'form': bound_form, 'profile': profile})
