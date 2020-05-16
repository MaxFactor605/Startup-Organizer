from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm
from django.http import HttpResponse
from django.contrib.messages import success


class ContactView(View):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_template_name = 'contact/contact_success.html'
    def get(self, request):
        return render(request, template_name=self.template_name, context={'form': self.form_class})

    def post(self, request):
        form_bound = self.form_class(request.POST)

        if form_bound.is_valid():
            mail_sent = form_bound.send_mail()
            if mail_sent:
                success(request, 'Email succesfully sent')
                return render(request, self.success_template_name)
        return render(request, template_name=self.template_name, context={'form': form_bound})
