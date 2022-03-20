from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

 
urlpatterns = [
    path('signup/', views.user_signup, name= "signup"), 
    path('login/', views.user_login, name= "login"),
    path('logout/', views.user_logout, name= "logout"),
    path('pswreset/', views.user_password_reset, name= 'pswreset'),
   	path('pswreset2/', views.user_password_reset2, name= 'pswreset2'),
    path('dashboard/', views.user_dashboard, name= "dashboard"),

    # email verification
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('reset/password/', PasswordResetView.as_view(template_name = 'authentication/resetpassword.html'), name='password_reset'),
    path('reset/password/done/', PasswordResetDoneView.as_view(template_name = 'authentication/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name = 'authentication/password_reset_complete.html' ), name='password_reset_complete'),


] 