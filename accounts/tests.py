from urllib import response
from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
from .views import SignUpView
from .forms import CustomUserCreationForm
# Create your tests here.


class CustomUserTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='lujain',
            email='l1@gmail.com',
            password='1234'
        )
        self.assertEqual(user.username, 'lujain')
        self.assertEqual(user.email, 'l1@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='lujain',
            email='l1@gmail.com',
            password='1234'
        )
        self.assertEqual(user.username, 'lujain')
        self.assertEqual(user.email, 'l1@gmail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class SignUpTest(TestCase):
    def setUp(self):
        self.sign_up_info = {
            'email':'kais.hasan314@gmail.com',
            'username':'kais',
            'password':'12345'
        }
        self.url = reverse('signup')
        self.response = self.client.post(self.url, self.sign_up_info)

    def test_signup_template(self):
        self.assertTemplateUsed(self.response, 'accounts/signup.html')
    
    def test_signup_view(self):
        view = resolve(self.url)
        self.assertEqual(
            view.func.__name__,
            SignUpView.as_view().__name__
        )
    
    def test_signup_then_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')


