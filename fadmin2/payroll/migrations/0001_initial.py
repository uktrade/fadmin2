# Generated by Django 2.0.2 on 2018-09-06 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('costcentre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminPayModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('year', models.IntegerField()),
                ('pay_rise', models.DecimalField(decimal_places=2, max_digits=18)),
                ('Vacancy', models.DecimalField(decimal_places=2, max_digits=18)),
                ('GAE', models.DecimalField(decimal_places=2, max_digits=18)),
                ('SCS_percent', models.DecimalField(decimal_places=2, max_digits=18)),
                ('SCS_number', models.DecimalField(decimal_places=2, max_digits=18)),
                ('indicative_budget', models.IntegerField()),
                ('group_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costcentre.DepartmentalGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DITPeople',
            fields=[
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('employee_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('isdirector', models.BooleanField(default=False, verbose_name='General Director/Director/Deputy Director')),
                ('isbusinesspartner', models.BooleanField(default=False, verbose_name='Business Partner')),
                ('cost_centre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='costcentre.CostCentre')),
            ],
            options={
                'verbose_name': 'DIT People',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('grade', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('gradedescription', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PayModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('year', models.IntegerField()),
                ('apr', models.DecimalField(decimal_places=1, max_digits=18)),
                ('may', models.DecimalField(decimal_places=1, max_digits=18)),
                ('jun', models.DecimalField(decimal_places=1, max_digits=18)),
                ('jul', models.DecimalField(decimal_places=1, max_digits=18)),
                ('aug', models.DecimalField(decimal_places=1, max_digits=18)),
                ('sep', models.DecimalField(decimal_places=1, max_digits=18)),
                ('oct', models.DecimalField(decimal_places=1, max_digits=18)),
                ('nov', models.DecimalField(decimal_places=1, max_digits=18)),
                ('dec', models.DecimalField(decimal_places=1, max_digits=18)),
                ('jan', models.DecimalField(decimal_places=1, max_digits=18)),
                ('feb', models.DecimalField(decimal_places=1, max_digits=18)),
                ('mar', models.DecimalField(decimal_places=1, max_digits=18)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payroll.Grade')),
                ('group_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costcentre.DepartmentalGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalaryMonthlyAverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_type', models.CharField(choices=[('CC', 'CostCentre'), ('DIR', 'Directorate'), ('DG', 'DepartmentalGroup')], max_length=50)),
                ('average_by', models.CharField(max_length=50)),
                ('average_value', models.DecimalField(decimal_places=2, max_digits=18)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payroll.Grade')),
            ],
        ),
        migrations.AddField(
            model_name='ditpeople',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payroll.Grade'),
        ),
    ]
