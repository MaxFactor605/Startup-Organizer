from django.shortcuts import get_object_or_404, render, redirect
from .models import Tag, Startup, NewsLink
from .forms import TagForm, StartupForm, NewsLinkForm
from django.views.generic import View
from .utils import DetailView, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class TagDetail(DetailView):
    model = Tag
    template_name = 'organizer/tag_detail.html'

class TagList(View):
    template_name = 'organizer/tag_list.html'
    paginate_by = 15
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


class StartupDetail(DetailView):
    model = Startup
    template_name = 'organizer/startup_detail.html'


class StartupList(View):
    page_kwarg = 'page'
    paginate_by = 8
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
        obj = self.get_object(**kwargs)
        redirect_link = obj.get_absolute_url()
        obj.delete()
        return redirect(redirect_link)


class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    redirect_url = 'organizer_tag_list'
