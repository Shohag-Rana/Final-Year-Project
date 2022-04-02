from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('profile/', views.student_profile, name= "student_profile"),
    path('logout/', views.student_logout, name= "student_logout"),
    path('student_pswreset/', views.student_password_reset, name= 'student_pswreset'),
   	path('student_pswreset2/', views.student_password_reset2, name= 'student_pswreset2'),


]
