from django.contrib import admin
from . models import Student

# Register your models here.
admin.site.register(Student)
class StudentModel(admin.ModelAdmin):
    list_display = ['username', 'dept']