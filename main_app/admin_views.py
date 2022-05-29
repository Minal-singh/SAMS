"""
View for admin to manage(update, create or delete) students, and get the record of attendance.
"""

from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from validate_email import validate_email
from django.contrib import messages
import datetime
import xlwt
import os
import shutil
from .filters import StudentFilter, AttendanceFilter, StudentAttendanceFilter
from .utils import validate_session
from .models import Attendance, Student, CustomUser
from django.conf import settings

BASE_DIR = settings.BASE_DIR

# render admin dashboard
def index(request):
    today = datetime.date.today()
    total_students = Student.objects.all().count()
    present_students = Attendance.objects.filter(date=today, present=True).count()
    absent_students = total_students - present_students
    context = {
        "total_students": total_students,
        "present_students": present_students,
        "absent_students": absent_students,
    }
    return render(request, "admin_templates/dashboard.html", context)


# to register student
def register_student(request):
    if request.GET and request.GET.get("reset", "") == "true":
        return HttpResponseRedirect(reverse("register_student"))
    context = {}
    if request.method == "POST":
        context = {"data": request.POST, "has_error": False}
        # get data from form
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender", "M")
        profile_pic = request.FILES.get("profile_pic", None)
        roll_no = request.POST.get("roll_no")
        course = request.POST.get("course")
        branch = request.POST.get("branch")
        session_start_year = request.POST.get("session_start_year")
        session_end_year = request.POST.get("session_end_year")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        session = ""

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, "Passwords should be atleast 6 characters long")
            context["has_error"] = True

        if password != password2:
            messages.add_message(request, messages.ERROR, "Passwords dont match")
            context["has_error"] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, "Please provide a valid email")
            context["has_error"] = True

        if validate_session(session_start_year, session_end_year):
            session = str(session_start_year) + "-" + str(session_end_year)

        else:
            messages.add_message(request, messages.ERROR, "Please provide a valid session")
            context["has_error"] = True

        try:
            if CustomUser.objects.get(email=email):
                messages.add_message(request, messages.ERROR, "Email is taken")
                context["has_error"] = True

        except Exception:
            pass

        try:
            if Student.objects.get(roll_no=roll_no):
                messages.add_message(request, messages.ERROR, "Roll number already exists")
                context["has_error"] = True

        except Exception:
            pass

        # if form has validation errors retain old data
        if context["has_error"]:
            return render(request, "admin_templates/register.html", context, status=400)

        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                user_type=2,
                first_name=first_name,
                last_name=last_name,
            )
            if profile_pic is not None:
                user.profile_pic = profile_pic
            user.gender = gender
            user.student.session = session
            user.student.roll_no = roll_no
            user.student.course = course
            user.student.branch = branch
            user.save()
            messages.add_message(request, messages.SUCCESS, "Successfully added")
            return redirect(reverse("register_student"))

        except Exception as e:
            messages.add_message(request, messages.ERROR, "Could not add: " + str(e))

    return render(request, "admin_templates/register.html", context)


# render list of students according to filters
def students(request):
    students = Student.objects.all()
    filter = StudentFilter(request.GET, queryset=students)
    students = filter.qs
    context = {"filter": filter, "students": students}
    return render(request, "admin_templates/students.html", context)


# detail of specific student along with his attendance
def student_detail(request, id):
    student = get_object_or_404(Student, user_id=id)
    # listing attendance for all days excluding sunday
    attendance_list = Attendance.objects.filter(student=student).exclude(date__week_day__in=[1])
    filter = StudentAttendanceFilter(request.GET, queryset=attendance_list)
    # to get attendance records within filter range
    attendance_list = filter.qs
    present_count = attendance_list.filter(present=True).count()
    end_date = request.GET.get("date_before", "")
    if end_date != "":
        end_date = datetime.date.fromisoformat(end_date)
    else:
        # if end date not mentioned in filter, then default will be today's date
        end_date = datetime.date.today()
    start_date = request.GET.get("date_after", "")
    if start_date != "":
        start_date = datetime.date.fromisoformat(start_date)
    else:
        # if end date not mentioned in filter, then default will be from 2nd Jan
        start_date = datetime.date.fromisoformat("2022-05-01")
    total_days = (end_date - start_date).days + 1
    absent_count = total_days - present_count
    context = {
        "student": student,
        "attendance_list": attendance_list,
        "filter": filter,
        "present_count": present_count,
        "absent_count": absent_count,
    }
    return render(request, "admin_templates/student_details.html", context)


# to edit student details
def edit_student(request, id):
    if request.GET and request.GET.get("reset", "") == "true":
        return HttpResponseRedirect(reverse("edit_student", kwargs={"id": id}))
    student = Student.objects.get(user_id=id)
    context = {"data": student}
    if request.method == "POST":
        # if once form is submitted override context
        context = {"data": request.POST, "has_error": False}
        # get data from form
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender", "M")
        profile_pic = request.FILES.get("profile_pic") or None
        roll_no = request.POST.get("roll_no")
        course = request.POST.get("course")
        branch = request.POST.get("branch")
        session_start_year = request.POST.get("session_start_year")
        session_end_year = request.POST.get("session_end_year")
        password = request.POST.get("password") or None
        password2 = request.POST.get("password2") or None
        session = ""

        if password is not None:
            if len(password) < 6:
                messages.add_message(request, messages.ERROR, "Passwords should be atleast 6 characters long")
                context["has_error"] = True

            if password != password2:
                messages.add_message(request, messages.ERROR, "Passwords dont match")
                context["has_error"] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, "Please provide a valid email")
            context["has_error"] = True

        if validate_session(session_start_year, session_end_year):
            session = str(session_start_year) + "-" + str(session_end_year)

        else:
            messages.add_message(request, messages.ERROR, "Please provide a valid session")
            context["has_error"] = True

        if student.user.email != email:
            try:
                if CustomUser.objects.get(email=email):
                    messages.add_message(request, messages.ERROR, "Email is taken")
                    context["has_error"] = True

            except Exception:
                pass

        if student.roll_no != roll_no:
            try:
                if Student.objects.get(roll_no=roll_no):
                    messages.add_message(request, messages.ERROR, "Roll number already exists")
                    context["has_error"] = True

            except Exception:
                pass

        # if form has validation errors retain old data
        if context["has_error"]:
            return render(request, "admin_templates/edit_student_details.html", context, status=400)

        try:
            user = CustomUser.objects.get(id=student.user_id)

            if profile_pic is not None:
                if os.path.exists(os.path.join(BASE_DIR, f"media/profile_picture/{str(id)}")):
                    shutil.rmtree(os.path.join(BASE_DIR, f"media/profile_picture/{str(id)}"))
                user.profile_pic = profile_pic

            if password is not None:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.gender = gender
            student.session = session
            student.roll_no = roll_no
            student.course = course
            student.branch = branch
            student.save()
            user.save()
            messages.add_message(request, messages.SUCCESS, "Successfully updated")
            return redirect(reverse("student_detail", kwargs={"id": id}))

        except Exception as e:
            messages.add_message(request, messages.ERROR, "Could not add: " + str(e))

    return render(request, "admin_templates/edit_student_details.html", context)


# to delete student
def delete_student(request, id):
    if request.method == "POST":
        student = get_object_or_404(Student, user_id=id)
        # if student has dataset created, delete it as well
        if os.path.exists(os.path.join(BASE_DIR, f"media/model_data/dataset/{str(id)}")):
            shutil.rmtree(os.path.join(BASE_DIR, f"media/model_data/dataset/{str(id)}"))
        student.delete()
        user = get_object_or_404(CustomUser, id=id)
        user.delete()
        messages.add_message(request, messages.SUCCESS, "Deleted successfully.")
    return HttpResponseRedirect(reverse(students))


# to get attendance report according to filters for all students
def attendance(request):
    attendance_list = Attendance.objects.all().exclude(date__week_day__in=[1])
    filter = AttendanceFilter(request.GET, queryset=attendance_list)
    attendance_list = filter.qs
    context = {"filter": filter, "attendance_list": attendance_list}

    # for exporting attendance to excel
    if request.POST:
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=Attendance" + str(datetime.datetime.now()) + ".xls"
        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Attendance")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ["First Name", "Last Name", "Email", "Course", "Branch", "Session", "Roll Number", "Date", "Present"]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = attendance_list.values_list(
            "student__user__first_name",
            "student__user__last_name",
            "student__user__email",
            "student__course",
            "student__branch",
            "student__session",
            "student__roll_no",
            "date",
            "present",
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response

    return render(request, "admin_templates/attendance.html", context)


# guide for FAQs and contact
def guide(request):
    return render(request, "admin_templates/guide.html")

# ====== DATA VISUALIZATION ======= #

def chart_data1(request):
    sessions = Student.objects.values_list("session", flat=True).order_by("session").distinct()
    data = {}
    for session in sessions:
        data[session] = Student.objects.filter(session=session).count()
    return JsonResponse({"data": data}, safe=False)


def chart_data2(request):
    branches = Student.objects.values_list("branch", flat=True).distinct()
    data = {}
    for branch in branches:
        data[branch] = Student.objects.filter(branch=branch).count()
    return JsonResponse({"data": data}, safe=False)


def chart_data3(request):
    courses = Student.objects.values_list("course", flat=True).distinct()
    data = {}
    for course in courses:
        data[course] = Student.objects.filter(course=course).count()
    return JsonResponse({"data": data}, safe=False)
