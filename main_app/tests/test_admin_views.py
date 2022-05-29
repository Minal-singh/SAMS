from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from ..models import CustomUser
from faker import Faker


class TestAdminViews(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.admin_email = self.faker.email()
        CustomUser.objects.create_superuser(email=self.admin_email, password="password")
        self.client.post(reverse("login"), {"email": self.admin_email, "password": "password"})

        self.password = "password"
        self.name = self.faker.name()
        self.first_name = self.name.split(" ")[0]
        self.last_name = " ".join(self.name.split(" ")[1:])
        self.user = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.faker.email(),
            "password": "password",
            "password2": "password",
            "gender": "F",
            "roll_no": "011ABC3040",
            "course": "B. Tech.",
            "branch": "CSE",
            "session_start_year": 2020,
            "session_end_year": 2024,
        }
        self.user2 = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.faker.email(),
            "password": "password",
            "password2": "password",
            "gender": "M",
            "roll_no": "011ABC3041",
            "course": "B.E.",
            "branch": "CSE",
            "session_start_year": 2020,
            "session_end_year": 2024,
        }

    def test_only_admin_should_access_admin_pages(self):
        CustomUser.objects.create_user(email="user@email.com", user_type=2, password="password")
        self.client.post(reverse("login"), {"email": "user@email.com", "password": "password"})
        response = self.client.get(reverse("admin_home"))
        self.assertEqual(response.status_code, 302)

    def test_should_show_dashboard(self):
        response = self.client.get(reverse("admin_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/dashboard.html")

    def test_should_show_students_page(self):
        response = self.client.get(reverse("students"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/students.html")

    def test_should_show_attendance_page(self):
        response = self.client.get(reverse("attendance"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/attendance.html")

    def test_should_show_register_page(self):
        response = self.client.get(reverse("register_student"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/register.html")

    def test_should_show_create_dataset_page(self):
        response = self.client.get(reverse("create_dataset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/create_dataset.html")

    def test_should_show_train_model_page(self):
        response = self.client.get(reverse("train_model"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/train_model.html")

    def test_should_show_mark_attendance_page(self):
        response = self.client.get(reverse("mark_attendance"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/mark_attendance.html")

    def test_should_show_guide_page(self):
        response = self.client.get(reverse("guide"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin_templates/guide.html")

    def test_should_register_student(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Successfully added", list(map(lambda x: x.message, storage)))

    def test_should_not_register_with_taken_email(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        response2 = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response2.status_code, 400)

        storage = get_messages(response2.wsgi_request)
        self.assertIn("Email is taken", list(map(lambda x: x.message, storage)))

    def test_should_not_register_with_short_password(self):
        self.user["password"] = "abc"
        self.user["password2"] = "abc"
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Passwords should be atleast 6 characters long", list(map(lambda x: x.message, storage)))

    def test_should_not_register_with_mismatched_password(self):
        self.user["password2"] = "Password"
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Passwords dont match", list(map(lambda x: x.message, storage)))

    def test_should_not_register_with_invalid_email(self):
        self.user["email"] = "Password"
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Please provide a valid email", list(map(lambda x: x.message, storage)))

    def test_should_not_register_with_taken_roll_no(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        response2 = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response2.status_code, 400)

        storage = get_messages(response2.wsgi_request)
        self.assertIn("Roll number already exists", list(map(lambda x: x.message, storage)))

    def test_should_not_register_with_invalid_session(self):
        self.user["session_end_year"] = 2019
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Please provide a valid session", list(map(lambda x: x.message, storage)))

        self.user["session_start_year"] = 2018
        self.user["session_end_year"] = 2025
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Please provide a valid session", list(map(lambda x: x.message, storage)))

    def test_should_edit_student_details(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        student = CustomUser.objects.get(email=self.user["email"])
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user2)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("student_detail", kwargs={"id": student.id}))

        storage = get_messages(response.wsgi_request)
        self.assertIn("Successfully updated", list(map(lambda x: x.message, storage)))

    def test_should_delete_student(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        student = CustomUser.objects.get(email=self.user["email"])
        response = self.client.post(reverse("delete_student",kwargs={"id": student.id}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("students"))

        storage = get_messages(response.wsgi_request)
        self.assertIn("Deleted successfully.", list(map(lambda x: x.message, storage)))


    def test_should_not_update_with_taken_email(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse("register_student"), self.user2)
        self.assertEquals(response.status_code, 302)

        student = CustomUser.objects.get(email=self.user["email"])
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user2)
        self.assertEquals(response.status_code, 400)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Email is taken", list(map(lambda x: x.message, storage)))

    def test_should_not_update_with_short_password(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)
        self.user["password"] = "abc"
        self.user["password2"] = "abc"
        student = CustomUser.objects.get(email=self.user["email"])
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Passwords should be atleast 6 characters long", list(map(lambda x: x.message, storage)))

    def test_should_not_update_with_mismatched_password(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)
        self.user["password2"] = "Password"
        student = CustomUser.objects.get(email=self.user["email"])
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Passwords dont match", list(map(lambda x: x.message, storage)))

    def test_should_not_update_with_invalid_email(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)
        self.user_email = self.user["email"]
        self.user["email"] = "Password"
        student = CustomUser.objects.get(email=self.user_email)
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Please provide a valid email", list(map(lambda x: x.message, storage)))

    def test_should_not_update_with_taken_roll_no(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse("register_student"), self.user2)
        self.assertEquals(response.status_code, 302)

        student = CustomUser.objects.get(email=self.user["email"])
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user2)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Roll number already exists", list(map(lambda x: x.message, storage)))

    def test_should_not_update_with_invalid_session(self):
        response = self.client.post(reverse("register_student"), self.user)
        self.assertEquals(response.status_code, 302)

        self.user["session_end_year"] = 2019
        student = CustomUser.objects.get(email=self.user["email"])
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Please provide a valid session", list(map(lambda x: x.message, storage)))

        self.user["session_start_year"] = 2018
        self.user["session_end_year"] = 2025
        response = self.client.post(reverse("edit_student", kwargs={"id": student.id}), self.user)
        self.assertEquals(response.status_code, 400)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Please provide a valid session", list(map(lambda x: x.message, storage)))

    # def test_should_reset_register_form(self):
    #     response = self.client.get(reverse("register_student"), {"reset":"true"})
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, reverse("register_student"))

    def tearDown(self):
        return super().tearDown()
