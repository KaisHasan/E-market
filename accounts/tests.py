from urllib import response
from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
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


class SignupTest(TestCase):
    username = 'lujain'
    email = 'l@gmail.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response,
            'account/signup.html'
        )
    
    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

