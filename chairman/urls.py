from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.chairman_profile, name="chairman_profile"),
    path('logout/', views.chairman_logout, name= "chairman_logout"),
    path('chairman_pswreset/', views.chairman_password_reset, name= 'chairman_pswreset'),
   	path('chairman_pswreset2/', views.chairman_password_reset2, name= 'chairman_pswreset2'),
   	path('teacher_list/', views.teacher_list, name= 'teacher_list'),
   	path('add_courses/', views.add_courses, name= 'add_courses'),
   	path('chairman_teacher_reg/', views.chairman_teacher_reg, name= 'chairman_teacher_reg'),
   	path('chairman_student_reg/', views.chairman_student_reg, name= 'chairman_student_reg'),
   	path('delete_faculty_page/', views.delete_faculty_page, name= 'delete_faculty_page'),
   	path('delete_student_page/', views.delete_student_page, name= 'delete_student_page'),
   	path('delete_current_faculty/<int:faculty_id>/', views.delete_current_faculty, name= 'delete_current_faculty'),
   	path('delete_current_student/<int:student_id>/', views.delete_current_student, name= 'delete_current_student'),
]