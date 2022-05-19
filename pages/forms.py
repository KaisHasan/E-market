from django import forms
from django.core.mail import send_mail, BadHeaderError


class ContactForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea())


    def send_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            subject = self.cleaned_data['subject']
            message = self.cleaned_data['message']
            try:
                send_mail(
                    subject,
                    message,
                    email,
                    ['hederamar@gmail.com']
                )
            except BadHeaderError:
                pass