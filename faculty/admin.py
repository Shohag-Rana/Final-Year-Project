from django.contrib import admin
from . models import Attendence_and_CT_Mark

# Register your models here.
@admin.register(Attendence_and_CT_Mark)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'student_name', 'course_teacher', 'ct_marks', 'attendence_marks']