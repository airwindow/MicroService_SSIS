# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_tenant_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='state',
            field=models.CharField(max_length=10),
        ),
    ]
