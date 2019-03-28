# Generated by Django 2.1.5 on 2019-03-25 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costcentre', '0016_auto_20190325_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCentreNextYear',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('cost_centre_code', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Cost Centre No.')),
                ('cost_centre_name', models.CharField(max_length=300, verbose_name='Cost Centre Name')),
            ],
            options={
                'verbose_name': 'Cost Centre (next financial year)',
                'verbose_name_plural': 'Cost Centres',
                'ordering': ['cost_centre_code'],
            },
        ),
        migrations.CreateModel(
            name='DepartmentalGroupNextYear',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('group_code', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Group No.')),
                ('group_name', models.CharField(max_length=300, verbose_name='Group Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DirectorateNextYear',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('directorate_code', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Directorate')),
                ('directorate_name', models.CharField(max_length=300, verbose_name='Directorate No.')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costcentre.DepartmentalGroupNextYear')),
            ],
            options={
                'verbose_name': 'Directorate',
                'verbose_name_plural': 'Directorates',
                'ordering': ['directorate_code'],
            },
        ),
        migrations.AddField(
            model_name='costcentrenextyear',
            name='directorate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costcentre.DirectorateNextYear'),
        ),
    ]
