from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from ..models import CustomUser
from faker import Faker


class TestStudentViews(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.admin_email = self.faker.email()
        CustomUser.objects.create_superuser(email=self.admin_email, password="password")
        self.client.post(reverse("login"), {"email": self.admin_email, "password": "password"})
        self.password = "password"
        self.name = self.faker.name()
        self.first_name = self.name.split(" ")[0]
        self.last_name = " ".join(self.name.split(" ")[1:])
        self.student_email = self.faker.email()
        self.user = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.student_email,
            "password": "password",
            "password2": "password",
            "gender": "F",
            "roll_no": "011ABC3040",
            "course": "B. Tech.",
            "branch": "CSE",
            "session_start_year": 2020,
            "session_end_year": 2024,
        }
        self.client.post(reverse("register_student"), self.user)
        self.client.post(reverse("logout"))
        self.client.post(reverse("login"), {"email": self.student_email, "password": "password"})

    def test_should_show_dashboard(self):
        response = self.client.get(reverse("student_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "student_templates/index.html")

    def test_should_show_attendance_page(self):
        response = self.client.get(reverse("student_attendance"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "student_templates/attendance.html")

    def test_should_update_password(self):
        self.data = {"old_password": "password", "password": "Password", "password2": "Password"}
        response = self.client.post(reverse("update_password"), self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        storage = get_messages(response.wsgi_request)
        self.assertIn("Password Updated successfully, login to continue", list(map(lambda x: x.message, storage)))

    def test_should_update_password_with_invalid_details(self):
        self.data = {"old_password": "passwor", "password": "Password", "password2": "Password"}
        response = self.client.post(reverse("update_password"), self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("student_home"))

        storage = get_messages(response.wsgi_request)
        self.assertIn("Please enter correct password", list(map(lambda x: x.message, storage)))

        self.data = {"old_password": "password", "password": "Password", "password2": "Passwor"}
        response = self.client.post(reverse("update_password"), self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("student_home"))

        storage = get_messages(response.wsgi_request)
        self.assertIn("Passwords dont match", list(map(lambda x: x.message, storage)))

        self.data = {"old_password": "password", "password": "Pass", "password2": "Pass"}
        response = self.client.post(reverse("update_password"), self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("student_home"))

        storage = get_messages(response.wsgi_request)
        self.assertIn("New password should be atleast 6 characters long", list(map(lambda x: x.message, storage)))

    def tearDown(self):
        return super().tearDown()
