# Generated by Django 3.2.9 on 2022-04-15 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0012_external_teacher_university_name'),
        ('chairman', '0010_running_semester_batch_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exteranal_Teacher_Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chairman.course')),
                ('external_teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.external_teacher')),
            ],
        ),
    ]
