from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserCreationForm, UserChangeForm
from django.urls import re_path
from django.contrib.messages import success
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import Profile


admin.site.unregister(get_user_model())

class ProfileAdminInline(admin.StackedInline):
    can_delete = False
    model = Profile
    exclude = ('slug',)

    def view_on_site(self, obj):
        return obj.get_absolute_url()



@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','date_joined', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('username', 'email')
    list_display_links = ('username', 'email')
    form = UserChangeForm
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    actions = ['make_staff']

    def make_staff(self, request, queryset):
        rows_updated = queryset.update(is_staff = True)
        if rows_updated == 1:
            message = '1 user was'
        else:
             message = '{0} users was'.format(rows_updated)
        message += ' succesfully made stuff'
        self.message_user(request, message)
    make_staff.short_description = ('Allow user to access Admin Site.')

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        return super().get_form(request, obj, **kwargs)

    #password
    change_password_form = AdminPasswordChangeForm
    change_user_password_template = ('admin/auth/user/change_password.html')

    def get_urls(self):
        password_change = [
            re_path(r'^(.+)/password/$', self.admin_site.admin_view(self.user_change_password), name='auth_user_password_change'),
        ]
        urls = super().get_urls()
        urls = password_change + urls
        return urls

    @method_decorator(sensitive_post_parameters())
    def user_change_password(self, request, user_id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(user_id))
        if user is None:
            raise Http404
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = (self.construct_change_message(request, form, None))
                self.log_change(request, user, change_message)
                success(request, 'Password changed')
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)
            context = {
                'title': 'Change password',
                'form_url': form_url,
                'form': form,
                'is_popup': IS_POPUP_VAR in request.POST
                            or IS_POPUP_VAR in request.GET,
                'opts': self.model._meta,
                'original': user,
            }
            context.update(admin.site.each_context(request))
            request.current_app = self.admin_site.name

            return TemplateResponse(request, self.change_user_password_template, context)
    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return tuple()
        inline_instance = ProfileAdminInline(self.model, self.admin_site)
        return inline_instance


