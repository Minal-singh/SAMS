"""
Views for students to check their attendance and profile, and restricting them to manipulate records.
"""

from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Student, Attendance
from .filters import StudentAttendanceFilter
import datetime


# to render student profile
def index(request):
    student = get_object_or_404(Student, user=request.user)
    context = {"student": student}
    return render(request, "student_templates/index.html", context)


# attendance records
def student_attendance(request):
    student = get_object_or_404(Student, user=request.user)
    attendance_list = Attendance.objects.filter(student=student).exclude(date__week_day__in=[1])
    filter = StudentAttendanceFilter(request.GET, queryset=attendance_list)
    attendance_list = filter.qs
    present_count = attendance_list.filter(present=True).count()
    end_date = request.GET.get("date_before", "")
    if end_date != "":
        end_date = datetime.date.fromisoformat(end_date)
    else:
        end_date = datetime.date.today()
    start_date = request.GET.get("date_after", "")
    if start_date != "":
        start_date = datetime.date.fromisoformat(start_date)
    else:
        start_date = datetime.date.fromisoformat("2022-05-01")
    total_days = (end_date - start_date).days + 1
    absent_count = total_days - present_count
    print(total_days, present_count, absent_count)
    context = {
        "attendance_list": attendance_list,
        "filter": filter,
        "present_count": present_count,
        "absent_count": absent_count,
    }
    return render(request, "student_templates/attendance.html", context)


# to change password
def change_password(request):
    if request.method == "POST":
        student = get_object_or_404(Student, user=request.user)
        old_password = request.POST.get("old_password")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not student.user.check_password(old_password):
            messages.add_message(request, messages.ERROR, "Please enter correct password")
            return HttpResponseRedirect(reverse("student_home"))

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, "New password should be atleast 6 characters long")
            return HttpResponseRedirect(reverse("student_home"))

        if password != password2:
            messages.add_message(request, messages.ERROR, "Passwords dont match")
            return HttpResponseRedirect(reverse("student_home"))

        try:
            student.user.set_password(password)
            student.user.save()
            messages.add_message(request, messages.SUCCESS, "Password Updated successfully, login to continue")
            return HttpResponseRedirect(reverse("login"))
        except Exception as e:
            messages.add_message(request, messages.ERROR, "Could not change: " + str(e))

    return HttpResponseRedirect(reverse("student_home"))
