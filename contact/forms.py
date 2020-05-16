from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers

class ContactForm(forms.Form):
    FEEDBACK = 'F'
    CORRECTION = 'C'
    SUPPORT = 'S'
    REASON_CHOICES = (
        (FEEDBACK, 'Feedback'),
        (CORRECTION, 'Correction'),
        (SUPPORT, 'support'),
    )
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
    reason = forms.ChoiceField(choices=REASON_CHOICES, initial=FEEDBACK)


    def send_mail(self):
        reason = self.cleaned_data['reason']
        reason_dict = dict(self.REASON_CHOICES)
        full_reason = reason_dict.get(reason)
        email = self.cleaned_data['email']
        text =self.cleaned_data['text']
        body = 'Message From: {0}\n\n{1}\n'.format(email, text)
        try:
            mail_managers(full_reason, body)
        except BadHeaderError:
            self.add_error(None, ValidationError('Could Not Send Email.\nExtra Headers not allowed in email body.', code='badheader'))
            return False
        else:
            return True
