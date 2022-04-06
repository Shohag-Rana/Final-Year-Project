from authentication.models import *
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm
from chairman.models import Course, Running_Semester, Roll_Sheet, Teacher_Student_Info

def student_profile(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        res = Student.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'student/profile.html', {'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

#logout
def student_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')


def student_password_reset(request):
    if request.user.is_authenticated:
        res = Student.objects.filter(email= request.user)
        student = Student.objects.get(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            fm = PasswordChangeForm(request.user)
            if request.method == 'POST':
                fm = PasswordChangeForm(user = request.user, data = request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                    return HttpResponseRedirect('/student/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'student/pswreset1.html', {'form': fm, 'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def student_password_reset2(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        res = Student.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            if request.method == 'POST':
                fm = SetPasswordForm(user= request.user, data= request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                    return HttpResponseRedirect('/student/profile/')
            else:
                fm = SetPasswordForm(request.user)
            return render(request, 'student/pswreset2.html', {'form': fm, 'student': student})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def current_courses(request):
    if request.user.is_authenticated:
        student = Student.objects.get(email= request.user)
        k = student.session
        running_semester = Running_Semester.objects.filter(session= k)
        for r in running_semester:
            semester = r.semester_no
        courses = Course.objects.filter(semister_no = semester)
        return render(request, 'student/current_courses.html', {'courses': courses, 'student':student})
    else:
        return HttpResponseRedirect('/')

def complete_courses(request):
    student = Student.objects.get(email= request.user)
    k = student.session
    running_semester = Running_Semester.objects.filter(session= k)
    for r in running_semester:
        semester = r.semester_no
    if semester == '4th Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester)
    if semester == '4th Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester')
    if semester == '3rd Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester')
    if semester == '3rd Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester')
    if semester == '2nd Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester')
    if semester == '2nd Year 1st Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 2nd Semester')
    if semester == '1st Year 2nd Semester':
        courses = Course.objects.filter().exclude(semister_no = semester).exclude(semister_no= '4th Year 2nd Semester').exclude(semister_no= '4th Year 1st Semester').exclude(semister_no= '3rd Year 2nd Semester').exclude(semister_no= '3rd Year 1st Semester').exclude(semister_no= '2nd Year 1st Semester')
    if semester == '1st Year 1st Semester':
        courses = Course.objects.all()
    return render(request, 'student/complete_courses.html', {'courses': courses, 'student':student})

def course_registration(request):
    student = Student.objects.get(email= request.user)
    session= student.session
    semester = Running_Semester.objects.get(session = session)
    sem = semester.semester_no
    courses = Course.objects.filter(semister_no = sem)
    course_code = []
    if request.method == 'POST':
        session = student.session
        student_id = student.student_id
        name_of_student = student.first_name + " " + student.last_name
        hall = student.hall
        remarks = 'Regular'
        for course in courses:
            course_code.append((course.course_code))
            c_code = course.course_code
            current_course = Course.objects.get(course_code = c_code)
            teacher = (current_course.course_teacher)
            credit = current_course.credit
            semister_no = current_course.semister_no
            course_name = current_course.course_name
            data = Teacher_Student_Info(
                student_name = name_of_student,
                student_id = student_id,
                course_name = course_name,
                course_code = c_code,
                teacher = teacher,
                hall = hall,
                session = session,
                credit = credit,
                )
            check_teacher_stu = Teacher_Student_Info.objects.filter(student_name= name_of_student, course_code = c_code, teacher = teacher)
            flag = False
            for check in check_teacher_stu:
                flag = True
            if flag == True:
                messages.warning(request, 'You are already registered this courses!!!')
            else:
                data.save()
                messages.success(request, 'course added successfully to the teacher')
        check = Roll_Sheet.objects.filter(student_id= student_id)
        flag = False
        for c in check:
            flag = True
        if flag == True:
            messages.warning(request, 'You are already registered in this semester!!!')
        else:
            data = Roll_Sheet(session= session, student_id= student_id, name_of_student= name_of_student, hall= hall, course_code= course_code, remarks= remarks)
            messages.success(request, 'one item added to the roll sheet')
            data.save()
    return render(request, 'student/course_registration.html',{'student':student, 'sem': sem, 'courses': courses})