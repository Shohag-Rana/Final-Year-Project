from django.urls import path
from . import views
# from . pdf import attendence_pdf, attendence_sheet_pdf

urlpatterns = [
    path('profile/', views.faculty_profile, name="faculty_profile"),
    path('faculty_pswreset/', views.faculty_pswreset, name="faculty_pswreset"),
    path('faculty_pswreset2/', views.faculty_pswreset2, name="faculty_pswreset2"),
    path('faculty_logout/', views.faculty_logout, name="faculty_logout"),
    path('current_course/', views.current_course, name="current_course"),
    path('course_details/<str:course_code>/', views.course_details, name="course_details"),
    path('attendence_sheet/<str:course_code>/', views.attendence_sheet, name="attendence_sheet"),
    path('ct_and_attendence_mark/<str:course_code>/', views.ct_and_attendence_mark, name="ct_and_attendence_mark"),
    path('student_ct_and_attendence_mark/<str:course_code>/', views.student_ct_and_attendence_mark, name="student_ct_and_attendence_mark"),
    path('edit_ct_and_attendence_mark/<str:course_code>/', views.edit_ct_and_attendence_mark, name="edit_ct_and_attendence_mark"),
    
    #pdf file url
    #path('attendence_pdf/', attendence_pdf, name="attendence_pdf"),
    #path('attendence_sheet_pdf/<str:course_code>/', attendence_sheet_pdf, name="attendence_sheet_pdf"),
]
