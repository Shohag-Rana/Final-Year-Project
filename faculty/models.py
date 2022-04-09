from django.db import models
from authentication.models import Teacher

# Create your models here.
class Attendence_and_CT_Mark(models.Model):
    student_id = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    session = models.CharField(max_length=200)
    semester_no = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    course_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    credit = models.FloatField()
    remarks = models.CharField(max_length=200)
    ct_marks = models.FloatField()
    attendence_marks = models.FloatField()
    total_ct_and_attendence_marks = models.FloatField() 