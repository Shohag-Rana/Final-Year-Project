# Generated by Django 3.2.9 on 2022-04-10 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chairman', '0008_registration_by_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration_by_semester',
            old_name='course_code',
            new_name='semester_name',
        ),
    ]
