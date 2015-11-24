# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(max_length=100)),
                ('courseID', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('courseID', 'studentID'),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentID', models.CharField(default=b'', max_length=100, serialize=False, primary_key=True)),
                ('lastName', models.CharField(default=b'', max_length=100, blank=True)),
                ('firstName', models.CharField(default=b'', max_length=100, blank=True)),
            ],
            options={
                'ordering': ('studentID',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('studentID', 'courseID')]),
        ),
    ]
