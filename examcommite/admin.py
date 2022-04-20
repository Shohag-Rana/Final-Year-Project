from django.contrib import admin
from . models import External_teacher_marks, Send_To_Third_Examinner, Third_Examinner_Marks
# Register your models here.

@admin.register(External_teacher_marks)
class External_teacher_marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'marks']

@admin.register(Send_To_Third_Examinner)
class Send_To_Third_Examinner_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'session']

@admin.register(Third_Examinner_Marks)
class Third_Examinner_Marks_ModelAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'course_code', 'session', 'marks']
