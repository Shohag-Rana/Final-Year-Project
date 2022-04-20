from django.contrib import admin
from . models import Attendence_and_CT_Mark, Theory_Marks

# Register your models here.
@admin.register(Attendence_and_CT_Mark)
class Attendence_and_CT_Mark_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'course_teacher', 'ct_marks', 'attendence_marks']

# theory
@admin.register(Theory_Marks)
class Theory_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'course_teacher', 'total_marks']