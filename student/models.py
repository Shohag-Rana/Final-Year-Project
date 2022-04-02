# from django.db import models
# from django.contrib.auth.models import User

# session_list = (
#     ('2012-13','2012-13'),
#     ('2013-14','2013-14'),
#     ('2014-15','2014-15'),
#     ('2015-16','2015-16'),
#     ('2016-17','2016-17'),
#     ('2017-18','2017-18'),
#     ('2018-19','2018-19'),
#     ('2019-20','2019-20'),
#     ('2020-21','2020-21'),
# )
# hall_name = (
#     ('JAMH', 'JAMH'),
#     ('BSMRH', 'BSMRH'),
#     ('SRH', 'SRH'),
#     ('AKH', 'AKH'),
#     ('BSFH', 'BSFH'),
# )

# class Student(User):
#     session = models.CharField(
#         choices= session_list,
#         max_length= 100,
#         default='2016-17',
#     )
#     student_id = models.CharField(max_length=10)
#     profile_image = models.ImageField(upload_to= "profileImage") 
#     hall = models.CharField(
#         max_length= 120,
#         choices= hall_name,
#         default= 'JAMH',
#     )
#     user_type = models.CharField(max_length= 100, default="student")

