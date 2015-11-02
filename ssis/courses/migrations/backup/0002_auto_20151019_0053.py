# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='id',
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='studentID',
            field=models.CharField(default=b'', max_length=100, serialize=False, primary_key=True),
        ),
    ]
