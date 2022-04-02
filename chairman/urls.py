from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.chairman_profile, name="chairman_profile"),
    path('logout/', views.chairman_logout, name= "chairman_logout"),
    path('chairman_pswreset/', views.chairman_password_reset, name= 'chairman_pswreset'),
   	path('chairman_pswreset2/', views.chairman_password_reset2, name= 'chairman_pswreset2'),
   	path('teacher_list/', views.teacher_list, name= 'teacher_list'),
   	path('add_courses/', views.add_courses, name= 'add_courses'),

]