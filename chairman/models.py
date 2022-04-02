from django.db import models
from authentication.models import Teacher
# Create your models here.

semister = (
    ('1st Year 1st Semester', '1st Year 1st Semester'),
    ('1st Year 2nd Semester', '1st Year 2nd Semester'),
    ('2nd Year 1st Semester', '2nd Year 1st Semester'),
    ('2nd Year 2nd Semester', '2nd Year 2nd Semester'),
    ('3rd Year 1st Semester', '3rd Year 1st Semester'),
    ('3rd Year 2nd Semester', '3rd Year 2nd Semester'),
    ('4th Year 1st Semester', '4th Year 1st Semester'),
    ('4th Year 2nd Semester', '4th Year 2nd Semester'),
)
course_types = (
    ('Theory', 'Theory'),
    ('Lab', 'Lab'),
    ('None', 'None'),
)


class Course(models.Model):
    course_name = models.CharField(max_length=150)
    course_code = models.CharField(max_length=150)
    course_type = models.CharField(
        max_length=200,
        choices= course_types,
        default= 'Theory'
        )
    credit = models.FloatField()
    semister_no = models.CharField(
        max_length=200,
        choices= semister,
        default= '1st Year 1st Semester'
        )
    course_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)