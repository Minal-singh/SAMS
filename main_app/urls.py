"""
Application level urls
"""

from django.urls import path
from . import views, admin_views, student_views, face_recognition_views

urlpatterns = [
    # main
    path("", views.index, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    # admin
    path("admin/dashboard/", admin_views.index, name="admin_home"),
    path("admin/students/", admin_views.students, name="students"),
    path("admin/attendance/", admin_views.attendance, name="attendance"),
    path("admin/students/<str:id>/", admin_views.student_detail, name="student_detail"),
    path("admin/register-student/", admin_views.register_student, name="register_student"),
    path("admin/edit-student/<str:id>/", admin_views.edit_student, name="edit_student"),
    path("admin/delete-student/<str:id>/", admin_views.delete_student, name="delete_student"),
    path("admin/guide/", admin_views.guide, name="guide"),
    # face_recognition
    path(
        "admin/create-dataset/",
        face_recognition_views.create_dataset,
        name="create_dataset",
    ),
    path(
        "admin/create-dataset/<str:id>/",
        face_recognition_views.create_dataset_for_student,
        name="create_dataset_for_student",
    ),
    path(
        "admin/delete-dataset/<str:id>/",
        face_recognition_views.delete_dataset_for_student,
        name="delete_dataset_for_student",
    ),
    path("admin/train-model/", face_recognition_views.train_model, name="train_model"),
    path(
        "admin/mark-attendance/",
        face_recognition_views.mark_attendance,
        name="mark_attendance",
    ),
    # chart data
    path("chart-data1", admin_views.chart_data1, name="chart_data1"),
    path("chart-data2", admin_views.chart_data2, name="chart_data2"),
    path("chart-data3", admin_views.chart_data3, name="chart_data3"),
    # student
    path("student/dashboard/", student_views.index, name="student_home"),
    path("student/attendance/", student_views.student_attendance, name="student_attendance"),
    path("student/update_password/", student_views.change_password, name="update_password"),
]
