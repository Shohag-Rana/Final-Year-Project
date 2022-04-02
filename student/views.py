from authentication.models import *
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm

def student_profile(request):
    if request.user.is_authenticated:
        res = Student.objects.filter(email= request.user)
        flag = False
        for r in res:
            flag = True
        if flag:
            return render(request, 'student/profile.html')
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
            return render(request, 'student/pswreset1.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/') 

def student_password_reset2(request):
    if request.user.is_authenticated:
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
            return render(request, 'student/pswreset2.html', {'form': fm})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/auth/login/')