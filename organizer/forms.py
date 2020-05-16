from django import forms
from .models import Tag, Startup, NewsLink


class SlugCleanMixin:
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise forms.ValidationError(('Slug name may not be "create".'))
        return new_slug


class TagForm(SlugCleanMixin, forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].lower()


class StartupForm(SlugCleanMixin, forms.ModelForm):
    class Meta:
        model = Startup
        fields = '__all__'


class NewsLinkForm(forms.ModelForm):
    class Meta:
        model = NewsLink
        fields = '__all__'

