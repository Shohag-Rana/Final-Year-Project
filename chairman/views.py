from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from authentication.models import *
from chairman.forms import CourseForm
from chairman.models import Course

# Create your views here.
def chairman_profile(request):
    if request.user.is_admin:
        return render(request, 'chairman/profile.html')
    else:
        return HttpResponseRedirect('/')

def chairman_password_reset(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            fm = PasswordChangeForm(request.user)
            if request.method == 'POST':
                fm = PasswordChangeForm(user=request.user, data=request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user)
                
                    return HttpResponseRedirect('/chairman/profile/')
            else:
                fm = PasswordChangeForm(request.user)
            return render(request, 'chairman/pswreset1.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')


def chairman_password_reset2(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            if request.method == 'POST':
                fm = SetPasswordForm(user=request.user, data=request.POST)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Password change successfully...')
                    update_session_auth_hash(request, fm.user) 
                    return HttpResponseRedirect('/chairman/profile/')
            else:
                fm = SetPasswordForm(request.user)
            return render(request, 'chairman/pswreset2.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')

#logout
def chairman_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

def teacher_list(request):
    if request.user.is_admin:
        teachers = Teacher.objects.all()
        return render(request, 'chairman/teacher_list.html', {'teachers': teachers})
    else:
        return HttpResponseRedirect('/')

def add_courses(request):
    allCourses = Course.objects.all()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course Added Successfull!!')
            return HttpResponseRedirect('/chairman/add_courses/')
        else:
            messages.warning(request, 'Your Enter Data is not Correct. Please re-enter again....')
            return HttpResponseRedirect('/chairman/add_courses/')
    form = CourseForm()
    return render(request, 'chairman/add_courses.html', {'form': form, 'courses': allCourses})