"""
Useful filter created for filtering data across application.
"""

from django import forms
import django_filters
from .models import Student, Attendance


class StudentFilter(django_filters.FilterSet):
    course = django_filters.AllValuesFilter(
        field_name="course", empty_label="Course", widget=forms.Select(attrs={"class": "form-control"})
    )
    branch = django_filters.AllValuesFilter(
        field_name="branch", empty_label="Branch", widget=forms.Select(attrs={"class": "form-control"})
    )
    session = django_filters.AllValuesFilter(
        field_name="session", empty_label="Session", widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Student
        fields = []


class AttendanceFilter(django_filters.FilterSet):
    course = django_filters.AllValuesFilter(
        field_name="student__course", empty_label="Course", widget=forms.Select(attrs={"class": "form-control"})
    )
    branch = django_filters.AllValuesFilter(
        field_name="student__branch", empty_label="Branch", widget=forms.Select(attrs={"class": "form-control"})
    )
    session = django_filters.AllValuesFilter(
        field_name="student__session", empty_label="Session", widget=forms.Select(attrs={"class": "form-control"})
    )
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Attendance
        fields = []


class StudentAttendanceFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Attendance
        fields = []
