# Generated by Django 3.2.9 on 2022-04-14 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_external_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='external_teacher',
            name='university_name',
            field=models.CharField(default='Dhaka University', max_length=250),
        ),
    ]
