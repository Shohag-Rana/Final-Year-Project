# Generated by Django 3.2.9 on 2022-04-07 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0005_roll_sheet_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher_student_info',
            name='remarks',
            field=models.CharField(default='Regular', max_length=150),
        ),
    ]
