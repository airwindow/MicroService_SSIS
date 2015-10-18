# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20151018_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseID', models.CharField(default=b'', max_length=100, serialize=False, primary_key=True)),
                ('courseTitle', models.CharField(default=b'', max_length=100, blank=True)),
                ('roomNum', models.CharField(default=b'', max_length=100, blank=True)),
            ],
            options={
                'ordering': ('courseID',),
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('courseID', models.ForeignKey(to='courses.Course')),
                ('studentID', models.ForeignKey(to='students.Student')),
            ],
            options={
                'ordering': ('courseID', 'studentID'),
            },
        ),
    ]
