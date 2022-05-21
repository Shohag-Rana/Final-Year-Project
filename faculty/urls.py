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
    path('lab_course_details/<str:course_code>/', views.lab_course_details, name="lab_course_details"),
    path('attendence_sheet/<str:course_code>/', views.attendence_sheet, name="attendence_sheet"),
    path('ct_and_attendence_mark/<str:course_code>/', views.ct_and_attendence_mark, name="ct_and_attendence_mark"),
    path('student_ct_and_attendence_mark/<str:course_code>/', views.student_ct_and_attendence_mark, name="student_ct_and_attendence_mark"),
    path('edit_ct_and_attendence_mark/<str:course_code>/', views.edit_ct_and_attendence_mark, name="edit_ct_and_attendence_mark"),
    path('Theory_mark_sheet/<str:course_code>/', views.Theory_mark_sheet, name="Theory_mark_sheet"),
    path('show_theory_marks/<str:course_code>/', views.show_theory_marks, name="show_theory_marks"),
    path('update_theory_marks/<str:course_code>/', views.update_theory_marks, name="update_theory_marks"),
    path('consolidated_marks_sheet/<str:course_code>/', views.consolidated_marks_sheet, name="consolidated_marks_sheet"),
    path('send_to_controller_theory_marks/<str:course_code>/', views.send_to_controller_theory_marks, name="send_to_controller_theory_marks"),
    path('lab_marks/<str:course_code>/', views.lab_marks, name="lab_marks"),
    path('final_50_marks/<str:course_code>/', views.final_50_marks, name="final_50_marks"),
    path('consoilated_lab_marksheet/<str:course_code>/', views.consoilated_lab_marksheet, name="consoilated_lab_marksheet"),
    path('show_lab_marks/<str:course_code>/', views.show_lab_marks, name="show_lab_marks"),
    path('edit_lab_marks/<str:course_code>/', views.edit_lab_marks, name="edit_lab_marks"),
    path('show_final_50_marks/<str:course_code>/', views.show_final_50_marks, name="show_final_50_marks"),
    path('edit_lab_final_50_marks/<str:course_code>/', views.edit_lab_final_50_marks, name="edit_lab_final_50_marks"),
    path('project_course_details/<str:course_code>/', views.project_course_details, name="project_course_details"),
    path('project_marks/<str:course_code>/', views.project_marks, name="project_marks"),
    path('viva_course_marks/<str:course_code>/', views.viva_course_marks, name="viva_course_marks"),
    path('research_project_marks/<str:course_code>/', views.research_project_marks, name="research_project_marks"),
    path('show_project_marks/<str:course_code>/', views.show_project_marks, name="show_project_marks"),
    path('show_viva_marks/<str:course_code>/', views.show_viva_marks, name="show_viva_marks"),
    path('show_research_project_marks/<str:course_code>/', views.show_research_project_marks, name="show_project_marks"),
    path('edit_project_marks/<str:course_code>/', views.edit_project_marks, name="edit_project_marks"),
    path('edit_viva_marks/<str:course_code>/', views.edit_viva_marks, name="edit_viva_marks"),
    path('edit_research_project_marks/<str:course_code>/', views.edit_research_project_marks, name="edit_research_project_marks"),
    path('consoilated_project_marksheet/<str:course_code>/', views.consoilated_project_marksheet, name="consoilated_project_marksheet"),
    path('consoilated_research_project_marksheet/<str:course_code>/', views.consoilated_research_project_marksheet, name="consoilated_research_project_marksheet"),
    path('research_project_course_details/<str:course_code>/', views.research_project_course_details, name="research_project_course_details"),
    path('viva_project_course_details/<str:course_code>/', views.viva_project_course_details, name="viva_project_course_details"),
    path('consoilated_viva_marksheet/<str:course_code>/', views.consoilated_viva_marksheet, name="consoilated_viva_marksheet"),
    #pdf file url
    #path('attendence_pdf/', attendence_pdf, name="attendence_pdf"),
    #path('attendence_sheet_pdf/<str:course_code>/', attendence_sheet_pdf, name="attendence_sheet_pdf"),
]
