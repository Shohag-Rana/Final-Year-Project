from django.db import models
from requests import session

# Create your models here.
class External_teacher_marks(models.Model):
    student_id = models.CharField(max_length= 150)
    course_code = models.CharField(max_length= 150)
    marks = models.FloatField()
    remarks = models.CharField(max_length= 150)
    session = models.CharField(max_length= 150)

class Send_To_Third_Examinner(models.Model):
    student_id = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    session = models.CharField(max_length=100)

class Third_Examinner_Marks(models.Model):
    student_id = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    marks = models.FloatField()