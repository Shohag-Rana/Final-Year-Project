from django.shortcuts import render, HttpResponseRedirect
from . models import Student
from . forms import StudentRegForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm

user_model = get_user_model()
# Create your views here.

#signup
def user_signup(request):
    if request.method == "POST":
        print('this is post req.')
        fm = StudentRegForm(request.POST, request.FILES)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            first_name = fm.cleaned_data['first_name']
            last_name = fm.cleaned_data['last_name']
            dept = fm.cleaned_data['dept']
            email = fm.cleaned_data['email']
            session = fm.cleaned_data['session']
            student_id = fm.cleaned_data['student_id']
            home_town = fm.cleaned_data['home_town']
            hall = fm.cleaned_data['hall']
            profile_image = fm.cleaned_data['profile_image']
            user = fm.save(commit = False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('authentication/account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                })
            send_mail = fm.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[send_mail])
            email.send()
            messages.success(request, 'Successfully created account')
            messages.success(request, 'Activate your account from email')

    else:
        fm = StudentRegForm()
    return render(request, 'authentication/signup.html', {'form': fm})

# activate your account
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_model._default_manager.get(pk= uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account activated now you can login')
        return HttpResponseRedirect('/auth/login/')
    else:
        messages.warning(request, 'activation link is invalid')
        return HttpResponseRedirect('/auth/signup/')

#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                nm = fm.cleaned_data['username']
                psw = fm.cleaned_data['password']
                user = authenticate(username=nm, password=psw)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'User Login Successfully!!')
                    return HttpResponseRedirect('/auth/dashboard/')
                else:
                    messages.error(request, 'wrong user enter correct one')
                    fm = LoginForm()
                    return render(request, 'authentication/login.html', {'form': fm})
        else:
            fm = LoginForm()
        return render(request, 'authentication/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/auth/dashboard/')

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

def user_dashboard(request):
    if request.user.is_authenticated:
        print(request.user.id)
        user = User.objects.get(pk= request.user.id)
        print(user)
        return render(request, 'authentication/profile.html', {'user': user})
    else:
        return HttpResponseRedirect('/auth/signup/')

def user_password_reset(request):

    if request.user.is_authenticated:
        fm = PasswordChangeForm(request.user)
        if request.method == 'POST':
            fm = PasswordChangeForm(user = request.user, data = request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Password change successfully...')
                update_session_auth_hash(request, fm.user)
                return HttpResponseRedirect('/auth/dashboard/')
        else:
            fm = PasswordChangeForm(request.user)
        return render(request, 'authentication/pswreset1.html', {'form': fm})
    else:
        return HttpResponseRedirect('/auth/login/') 

def user_password_reset2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user= request.user, data= request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Password change successfully...')
                update_session_auth_hash(request, fm.user)
                return HttpResponseRedirect('/auth/dashboard/')
        else:
            fm = SetPasswordForm(request.user)
        return render(request, 'authentication/pswreset2.html', {'form': fm})
    else:
        return HttpResponseRedirect('/auth/login/')