# Generated by Django 3.2.9 on 2022-05-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examcommite', '0003_third_examinner_marks'),
    ]

    operations = [
        migrations.CreateModel(
            name='External_Teacher_Research_Project_Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=200)),
                ('student_name', models.CharField(max_length=200)),
                ('session', models.CharField(max_length=200)),
                ('semester_no', models.CharField(max_length=200)),
                ('course_code', models.CharField(max_length=200)),
                ('course_name', models.CharField(max_length=200)),
                ('credit', models.FloatField()),
                ('remarks', models.CharField(max_length=200)),
                ('supervisor_marks', models.FloatField()),
                ('defence_marks', models.FloatField()),
                ('total_mark', models.FloatField()),
            ],
        ),
    ]
