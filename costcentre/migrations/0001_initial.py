# Generated by Django 2.1.1 on 2018-10-03 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CostCentre',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cost_centre_code', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Cost Centre Code')),
                ('cost_centre_name', models.CharField(max_length=300, verbose_name='Cost Centre Name')),
            ],
            options={
                'verbose_name': 'Cost Centre',
                'verbose_name_plural': 'Cost Centres',
            },
        ),
        migrations.CreateModel(
            name='DepartmentalGroup',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('group_code', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Group')),
                ('group_name', models.CharField(max_length=300, verbose_name='Group Name')),
            ],
            options={
                'verbose_name': 'Departmental Group',
                'verbose_name_plural': 'Departmental Groups',
            },
        ),
        migrations.CreateModel(
            name='Directorate',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('directorate_code', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Directorate')),
                ('directorate_name', models.CharField(max_length=300, verbose_name='Directorate Name')),
            ],
            options={
                'verbose_name': 'Directorate',
                'verbose_name_plural': 'Directorates',
            },
        ),
    ]
