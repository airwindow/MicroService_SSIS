# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.CharField(default=b'', max_length=100, blank=True)),
                ('lastName', models.CharField(default=b'', max_length=100, blank=True)),
                ('firstName', models.CharField(default=b'', max_length=100, blank=True)),
            ],
        ),
    ]
