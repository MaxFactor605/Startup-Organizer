from django.http import Http404, HttpResponseRedirect


class PostFormValidMixin:
    def form_valid(self, form):
        self.object = form.save(self.request)
        return HttpResponseRedirect(self.get_succes_url())
