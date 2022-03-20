# Generated by Django 3.2.9 on 2022-03-20 03:53

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('departement', models.CharField(max_length=100)),
                ('session', models.CharField(choices=[('2012-13', '2012-13'), ('2013-14', '2013-14'), ('2014-15', '2014-15'), ('2015-16', '2015-16'), ('2016-17', '2016-17'), ('2017-18', '2017-18'), ('2018-19', '2018-19'), ('2019-20', '2019-20'), ('2020-21', '2020-21')], default='2016-17', max_length=100)),
                ('student_id', models.CharField(max_length=10)),
                ('home_town', models.CharField(max_length=200)),
                ('profile_image', models.ImageField(upload_to='profileImage')),
                ('hall', models.CharField(choices=[('JAMH', 'JAMH'), ('BSMRH', 'BSMRH'), ('SRH', 'SRH'), ('AKH', 'AKH'), ('BSFH', 'BSFH')], default='JAMH', max_length=120)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
