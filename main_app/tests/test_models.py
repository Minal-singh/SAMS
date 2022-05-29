from django.shortcuts import get_object_or_404
from django.test import TestCase
from ..models import CustomUser, Admin, Student, Attendance
from faker import Faker


class TestModels(TestCase):
    def test_customuser_model(self):
        self.faker = Faker()
        self.name = self.faker.name()
        self.first_name = self.name.split(" ")[0]
        self.last_name = " ".join(self.name.split(" ")[1:])
        user = CustomUser.objects.create_user(
            first_name=self.first_name, last_name=self.last_name, email=self.faker.email(), password="password"
        )
        user.save()
        self.assertEqual(str(user), self.name)

        profile_pic_directory_path = user.get_profile_pic_directory_path("abc.png")
        self.assertEqual(profile_pic_directory_path, "profile_pictures/{}/{}.png".format(str(user.id), str(user.id)))

    def test_admin_model(self):
        self.faker = Faker()
        self.user_email = self.faker.email()
        user = CustomUser.objects.create_superuser(email=self.user_email, password="password")
        self.user_id = user.id
        user.save()
        admin = get_object_or_404(Admin, user_id=self.user_id)
        self.assertEqual(str(admin), self.user_email)

    def test_student_model(self):
        self.faker = Faker()
        self.name = self.faker.name()
        self.first_name = self.name.split(" ")[0]
        self.last_name = " ".join(self.name.split(" ")[1:])
        self.user_email = self.faker.email()
        user = CustomUser.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.user_email,
            user_type=2,
            gender="F",
            password="password",
        )
        self.user_id = user.id
        user.save()
        student = get_object_or_404(Student, user_id=self.user_id)
        self.assertEqual(str(student), self.user_email)

    def test_attendance_model(self):
        self.faker = Faker()
        user = CustomUser.objects.create_user(
            email=self.faker.email(),
            user_type=2,
            password="password",
        )
        self.user_id = user.id
        user.save()
        student = get_object_or_404(Student, user_id=self.user_id)
        todays_attendance = Attendance(student=student, present=True)
        self.assertEqual(str(todays_attendance), str(todays_attendance.date))
