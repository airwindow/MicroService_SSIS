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
                ('ssn', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('balance', models.CharField(default=b'0.0', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('tenant_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('university', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TenantAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute_name', models.CharField(max_length=30)),
                ('attribute_type', models.CharField(max_length=30)),
                ('tenant', models.ForeignKey(to='finance.Tenant')),
            ],
        ),
        migrations.CreateModel(
            name='TenantAttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute_value', models.CharField(max_length=100)),
                ('student', models.ForeignKey(to='finance.Student')),
                ('tenant', models.ForeignKey(to='finance.Tenant')),
                ('tenant_attribute', models.ForeignKey(to='finance.TenantAttribute')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='tenant',
            field=models.ForeignKey(to='finance.Tenant'),
        ),
    ]
