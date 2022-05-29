from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from ..models import CustomUser
from faker import Faker


class TestViews(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user_email = self.faker.email()
        self.password = "password"
        user = CustomUser.objects.create_user(email=self.user_email, password=self.password)
        user.save()

    def test_should_redirect_to_login_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_should_show_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/login.html")

    def test_should_login_successfully(self):
        user = CustomUser.objects.first()
        response = self.client.post(reverse("login"), {"email": user.email, "password": "password"})
        self.assertEquals(response.status_code, 302)

    def test_should_not_login_with_invalid_password(self):
        user = CustomUser.objects.first()
        response = self.client.post(reverse("login"), {"email": user.email, "password": "Password"})
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)

        self.assertIn("Invalid login credentials", list(map(lambda x: x.message, storage)))

    def test_should_not_login_with_empty_form(self):
        response = self.client.post(reverse("login"), {"email": "", "password": ""})
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Email is required", list(map(lambda x: x.message, storage)))
        self.assertIn("Password is required", list(map(lambda x: x.message, storage)))

    def test_should_redirect_admin_to_admin_dashboard(self):
        self.faker = Faker()
        self.user_email = self.faker.email()
        self.password = "password"
        user = CustomUser.objects.create_superuser(email=self.user_email, user_type=1, password=self.password)
        user.save()
        response = self.client.post(reverse("login"), {"email": self.user_email, "password": self.password})
        self.assertRedirects(response, reverse("admin_home"))

    def test_should_redirect_admin_to_student_dashboard(self):
        self.faker = Faker()
        self.user_email = self.faker.email()
        self.password = "password"
        user = CustomUser.objects.create_user(email=self.user_email, user_type=2, password=self.password)
        user.save()
        response = self.client.post(reverse("login"), {"email": self.user_email, "password": self.password})
        self.assertRedirects(response, reverse("student_home"))

    def test_should_logout_user(self):
        user = CustomUser.objects.first()
        self.client.post(reverse("login"), {"email": user.email, "password": "password"})
        response = self.client.get("/logout/")
        self.assertRedirects(response, reverse("login"))

    def tearDown(self):
        return super().tearDown()
