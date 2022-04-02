from django.contrib import admin
from . models import Course

# Register your models here.
@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name']