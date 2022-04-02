from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.faculty_profile, name="faculty_profile"),
    path('faculty_pswreset/', views.faculty_pswreset, name="faculty_pswreset"),
    path('faculty_pswreset2/', views.faculty_pswreset2, name="faculty_pswreset2"),
    path('faculty_logout/', views.faculty_logout, name="faculty_logout"),
    path('current_course/', views.current_course, name="current_course"),
]
