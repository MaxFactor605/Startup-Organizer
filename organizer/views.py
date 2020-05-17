from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from .models import Tag, Startup, NewsLink
from django.template import loader
from django.shortcuts import reverse
from .forms import TagForm, StartupForm, NewsLinkForm
from django.views.generic import View
from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug__iexact=slug)
    return render(request, 'organizer/tag_detail.html', context={'tag': tag})


class TagList(View):
    template_name = 'organizer/tag_list.html'
    paginate_by = 5
    page_kwarg = 'page'


    def get(self, request):
        page_number = request.GET.get(self.page_kwarg)
        paginator = Paginator(Tag.objects.all(), self.paginate_by)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return render(request, self.template_name, context={'tag_list': page, 'paginator': paginator})


def startup_detail(request, slug):
    startup = get_object_or_404(Startup, slug__iexact=slug)
    return render(request, 'organizer/startup_detail.html', context={'startup': startup})


class StartupList(View):
    page_kwarg = 'page'
    paginate_by = 5
    template_name = 'organizer/startup_list.html'
    def get(self, request):
        page_number = request.GET.get(self.page_kwarg)
        paginator = Paginator(Startup.objects.all(), self.paginate_by)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return render(request, self.template_name, context={'startup_list': page, 'paginator': paginator})


class TagCreate(ObjectCreateMixin, View):
    form_class = TagForm
    template_name = 'organizer/tag_create.html'


class StartupCreate(ObjectCreateMixin, View):
    form_class = StartupForm
    template_name = 'organizer/startup_create.html'


class NewsLinkCreate(ObjectCreateMixin, View):
    form_class = NewsLinkForm
    template_name = 'organizer/newslink_create.html'


class NewsLinkUpdate(ObjectUpdateMixin, View):
    form_class = NewsLinkForm
    model = NewsLink
    template_name = 'organizer/newslink_update.html'


class StartupUpdate(ObjectUpdateMixin, View):
    form_class = StartupForm
    model = Startup
    template_name = 'organizer/startup_update.html'


class TagUpdate(ObjectUpdateMixin, View):
    form_class = TagForm
    model = Tag
    template_name = 'organizer/tag_update.html'


class StartupDelete(ObjectDeleteMixin, View):
    model = Startup
    redirect_url = 'organizer_startup_list'

class NewslinkDelete(ObjectDeleteMixin, View):
    model = NewsLink

    def get_object(self, **kwargs):
        return get_object_or_404(self.model, **kwargs)

    def post(self, request, **kwargs):
        object = self.get_object(**kwargs)
        redirect_link = object.get_absolute_url()
        object.delete()
        return redirect(redirect_link)

class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    redirect_url = 'organizer_tag_list'