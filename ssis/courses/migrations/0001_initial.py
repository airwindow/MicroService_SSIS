# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
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
                ('courseID', models.CharField(max_length=100)),
                ('studentID', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('courseID', 'studentID'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('courseID', 'studentID')]),
        ),
    ]
