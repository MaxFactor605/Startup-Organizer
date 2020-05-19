from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
class DetailView(View):
    model = None
    template_name = ''

    def get_object(self, slug):
        return get_object_or_404(self.model, slug__iexact=slug)

    def get(self, request, slug):
        obj = self.get_object(slug)
        return render(request, self.template_name, context={self.model.__name__.lower(): obj})


class ObjectCreateMixin:
    form_class = None
    template_name = ''

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_object = bound_form.save()
            return redirect(new_object)
        else:
            return render(request, self.template_name, context={'form': bound_form})


class ObjectUpdateMixin:
    form_class = None
    model = None
    template_name = ''

    def get_object(self, **kwargs):
        return get_object_or_404(self.model, **kwargs)

    def get(self, request, **kwargs):
        object = self.get_object(**kwargs)
        return render(request, self.template_name, context={'form': self.form_class(instance=object), self.model.__name__.lower(): object})

    def post(self, request, **kwargs):
        object = self.get_object(**kwargs)
        bound_form = self.form_class(request.POST, instance=object)
        if bound_form.is_valid():
            new_link = bound_form.save()
            return redirect(new_link)
        else:
            return render(request, self.template_name, context={'form': bound_form, self.model.__name__.lower(): object})

class ObjectDeleteMixin:
    model = None
    redirect_url = ''
    def get_object(self, **kwargs):
        return get_object_or_404(self.model, **kwargs)

    def post(self, request, **kwargs):
        object = self.get_object(**kwargs)
        object.delete()
        return redirect(self.redirect_url)