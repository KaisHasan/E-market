from urllib import request
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class ContactUsView(FormView):
    template_name = 'pages/contact_us.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
