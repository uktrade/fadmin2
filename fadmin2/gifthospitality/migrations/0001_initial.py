# Generated by Django 2.0.2 on 2018-07-04 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('costcentre', '0001_initial'),
        ('chartofaccountDIT', '0001_initial'),
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftsAndHospitality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
        ),
        migrations.CreateModel(
            name='HotelAndTravel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traveller_name', models.CharField(max_length=500)),
                ('product_type', models.CharField(max_length=500)),
                ('room_nights', models.IntegerField()),
                ('travel_date', models.CharField(max_length=10)),
                ('routing', models.CharField(max_length=500)),
                ('geog_indicator', models.CharField(max_length=500)),
                ('hotel_city', models.CharField(max_length=500)),
                ('class_of_service', models.CharField(max_length=500)),
                ('rail_journey_type', models.CharField(max_length=500)),
                ('hotel_name', models.CharField(max_length=500)),
                ('supplier_name', models.CharField(max_length=500)),
                ('fee_paid', models.DecimalField(decimal_places=2, max_digits=18)),
                ('int_dom', models.CharField(max_length=500)),
                ('reason_code_desc', models.CharField(max_length=500)),
                ('cost_centre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costcentre.CostCentre')),
                ('natural_account_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chartofaccountDIT.NaturalCode')),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costcentre.Programme')),
            ],
        ),
    ]
