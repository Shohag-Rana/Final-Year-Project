
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from authentication.models import *
from chairman.models import Course, Teacher_Student_Info
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
    context = {
        'c_code': c_code,
        'c_name': c_name,
        'c_credit': c_credit,
        'students': students,
    }
    return render(request, 'faculty/course_details.html', context)