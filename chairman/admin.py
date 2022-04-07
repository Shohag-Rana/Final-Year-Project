from django.contrib import admin
from . models import Course, Running_Semester, Roll_Sheet, Teacher_Student_Info

# Register your models here.
@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'course_teacher']

@admin.register(Running_Semester)
class Running_SemesterModelAdmin(admin.ModelAdmin):
    list_display = ['semester_no', 'session']

@admin.register(Roll_Sheet)
class Roll_Sheet_ModelAdmin(admin.ModelAdmin):
    list_display = ['session', 'student_id']

@admin.register(Teacher_Student_Info)
class Teacher_Student_Info_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code']