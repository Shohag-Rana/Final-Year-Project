
from tokenize import Number
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from authentication.models import *
from chairman.models import Course, Teacher_Student_Info
from . models import Attendence_and_CT_Mark
# Create your views here.
def faculty_profile(request):
    if request.user.is_authenticated:
        res = Teacher.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'faculty/profile.html', {'faculty': res})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def faculty_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

def faculty_pswreset(request):
    if request.user.is_authenticated:
        res = Teacher.objects.filter(email= request.user)
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
                    return HttpResponseRedirect('/faculty/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'faculty/pswreset1.html', {'form': fm, 'faculty': res})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def faculty_pswreset2(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            res = Teacher.objects.filter(email= request.user)
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
                        return HttpResponseRedirect('/faculty/profile/')
                else:
                    fm = SetPasswordForm(request.user)
                return render(request, 'faculty/pswreset2.html', {'form': fm, 'faculty': res})
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

def current_course(request):
    if request.user.is_authenticated:
        user = request.user
        faculty = Teacher.objects.filter(email= request.user)
        courses = Course.objects.filter(course_teacher = user)
        return render(request, 'faculty/current_course.html', {'courses': courses, 'faculty': faculty})
    else:
        return HttpResponseRedirect('/')

def course_details(request, course_code):
    students = Teacher_Student_Info.objects.filter(course_code = course_code)
    course = Course.objects.get(course_code= course_code)
    c_code = (course.course_code)
    c_name = (course.course_name)
    c_credit = (course.credit)
    c_teacher = course.course_teacher
    context = {
        'c_code': c_code,
        'c_name': c_name,
        'c_credit': c_credit,
        'students': students,
        'c_teacher': c_teacher,
    }
    return render(request, 'faculty/course_details.html', context)

def attendence_sheet(request, course_code):
    course = Course.objects.get(course_code= course_code)
    students = Teacher_Student_Info.objects.filter(course_code= course_code)
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'students': students,
    }
    return render(request, 'faculty/attendence_sheet.html', context)

def ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    students = Teacher_Student_Info.objects.filter(course_code= course_code)
    ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
    for check in ct_attend_marks:
        return HttpResponseRedirect(f'/faculty/edit_ct_and_attendence_mark/{course_code}/') 
    context = {
        'semister_no': course.semister_no,
        'c_code': course_code,
        'c_teacher': course.course_teacher,
        'credit': course.credit,
        'c_name': course.course_name,
        'students': students,
        'ct_attend_marks': ct_attend_marks,
        }
    if request.method == 'POST':
        course = Course.objects.get(course_code= course_code)
        students = Teacher_Student_Info.objects.filter(course_code= course_code)
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
        context = {
            'semister_no': course.semister_no,
            'c_code': course_code,
            'c_teacher': course.course_teacher,
            'credit': course.credit,
            'c_name': course.course_name,
            'students': students,
            'ct_attend_marks': ct_attend_marks,
            }
        for student in students:
            ct_marks = request.POST.get(f'{student.student_id}')
            attend_marks = request.POST.get(f'{student.student_name}')
            if ct_marks and attend_marks:
                ct_marks = (int(ct_marks))
                attend_marks = (int(attend_marks))
                if ct_marks > 20 or attend_marks > 10:
                    messages.warning(request, 'ct marks can not greater than 20 and attendence mark can not grater than 10')
                    return HttpResponseRedirect(f'/faculty/ct_and_attendence_mark/{course_code}/')       
            else:
                ct_marks = 0
                attend_marks = 0
            student_id = student.student_id
            student_name = student.student_name
            session = student.session
            semester_no = course.semister_no
            course_code = course_code
            course_name = course.course_name
            course_teacher = course.course_teacher
            credit = course.credit
            remarks = student.remarks
            ct_marks = ct_marks
            attendence_marks = attend_marks
            total_ct_and_attendence_marks = ct_marks + attendence_marks
            checker = Attendence_and_CT_Mark.objects.filter(student_id= student_id, course_code=course_code, course_teacher= course.course_teacher)
            flag = False
            for c in checker:
                id = c.id
                data = Attendence_and_CT_Mark(id=id,student_id = student_id,student_name = student_name,session = session,semester_no = semester_no,course_code = course_code,course_name = course_name,course_teacher = course_teacher,credit = credit,remarks =remarks,ct_marks = ct_marks,attendence_marks = attendence_marks,total_ct_and_attendence_marks = total_ct_and_attendence_marks)
                data.save()
                flag = True
            if flag == False:
                data = Attendence_and_CT_Mark(
                    student_id = student_id,
                    student_name = student_name,
                    session = session,
                    semester_no = semester_no,
                    course_code = course_code,
                    course_name = course_name,
                    course_teacher = course_teacher,
                    credit = credit,
                    remarks =remarks,
                    ct_marks = ct_marks,
                    attendence_marks = attendence_marks,
                    total_ct_and_attendence_marks = total_ct_and_attendence_marks
                    )
                data.save()
        messages.success(request,'CT and Attendence Mark Added Successfully!!!!')
        return HttpResponseRedirect(f'/faculty/student_ct_and_attendence_mark/{course_code}/')  
    return render(request, 'faculty/ct_and_attendence_mark.html', context)

def student_ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'student_ct_and_attend_marks': student_ct_and_attend_marks,
    }
    return render(request, 'faculty/student_ct_and_attendence_mark.html', context)

def edit_ct_and_attendence_mark(request, course_code):
    course = Course.objects.get(course_code= course_code)
    student_ct_and_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
    context = {
        'course_code': course_code,
        'course_name': course.course_name,
        'credit': course.credit,
        'semester_no': course.semister_no,
        'course_teacher': course.course_teacher,
        'student_ct_and_attend_marks': student_ct_and_attend_marks,
    }
    if request.method == 'POST':
        course = Course.objects.get(course_code= course_code)
        students = Teacher_Student_Info.objects.filter(course_code= course_code)
        ct_attend_marks = Attendence_and_CT_Mark.objects.filter(course_code= course_code)
        context = {
            'semister_no': course.semister_no,
            'c_code': course_code,
            'c_teacher': course.course_teacher,
            'credit': course.credit,
            'c_name': course.course_name,
            'students': students,
            'ct_attend_marks': ct_attend_marks,
            }
        for student in students:
            ct_marks = request.POST.get(f'{student.student_id}')
            attend_marks = request.POST.get(f'{student.student_name}')
            if ct_marks and attend_marks:
                ct_marks = (float(ct_marks))
                attend_marks = (float(attend_marks))
                if ct_marks > 20 or attend_marks > 10:
                    messages.warning(request, 'ct marks can not greater than 20 and attendence mark can not grater than 10')
                    return HttpResponseRedirect(f'/faculty/edit_ct_and_attendence_mark/{course_code}/')       
            else:
                ct_marks = 0
                attend_marks = 0
            student_id = student.student_id
            student_name = student.student_name
            session = student.session
            semester_no = course.semister_no
            course_code = course_code
            course_name = course.course_name
            course_teacher = course.course_teacher
            credit = course.credit
            remarks = student.remarks
            ct_marks = ct_marks
            attendence_marks = attend_marks
            total_ct_and_attendence_marks = ct_marks + attendence_marks
            checker = Attendence_and_CT_Mark.objects.filter(student_id= student_id, course_code=course_code, course_teacher= course.course_teacher)
            flag = False
            for c in checker:
                id = c.id
                data = Attendence_and_CT_Mark(id=id,student_id = student_id,student_name = student_name,session = session,semester_no = semester_no,course_code = course_code,course_name = course_name,course_teacher = course_teacher,credit = credit,remarks =remarks,ct_marks = ct_marks,attendence_marks = attendence_marks,total_ct_and_attendence_marks = total_ct_and_attendence_marks)
                data.save()
                flag = True
            if flag == False:
                data = Attendence_and_CT_Mark(
                    student_id = student_id,
                    student_name = student_name,
                    session = session,
                    semester_no = semester_no,
                    course_code = course_code,
                    course_name = course_name,
                    course_teacher = course_teacher,
                    credit = credit,
                    remarks =remarks,
                    ct_marks = ct_marks,
                    attendence_marks = attendence_marks,
                    total_ct_and_attendence_marks = total_ct_and_attendence_marks
                    )
                data.save()
        messages.success(request,'CT and Attendence Mark Added Successfully!!!!')
        return HttpResponseRedirect(f'/faculty/student_ct_and_attendence_mark/{course_code}/') 
    return render(request, 'faculty/edit_ct_and_attendence_mark.html', context)

