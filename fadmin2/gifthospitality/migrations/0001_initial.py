# Generated by Django 2.0.2 on 2018-09-05 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('costcentre', '0002_auto_20180905_1535'),
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftsAndHospitality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('classification', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('date_offered', models.DateTimeField()),
                ('venue', models.CharField(max_length=1000)),
                ('reason', models.CharField(max_length=1000)),
                ('value', models.DecimalField(decimal_places=2, max_digits=18)),
                ('band', models.CharField(max_length=50)),
                ('rep', models.CharField(max_length=255)),
                ('offer', models.CharField(max_length=50)),
                ('company_rep', models.CharField(max_length=50)),
                ('company', models.CharField(max_length=255)),
                ('action_taken', models.CharField(max_length=50)),
                ('date_stamp', models.DateTimeField()),
                ('entered_by', models.CharField(max_length=50)),
                ('staff_no', models.CharField(max_length=50)),
                ('entered_date_stamp', models.DateTimeField()),
                ('category', models.CharField(max_length=255)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payroll.Grade')),
                ('group_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costcentre.DepartmentalGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
