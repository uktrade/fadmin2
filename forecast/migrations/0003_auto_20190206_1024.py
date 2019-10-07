# Generated by Django 2.1.5 on 2019-02-06 10:24

from django.db import migrations

def populate_year(apps, schema_editor):
    YearModel = apps.get_model('forecast', 'FinancialYear')
    obj, created = YearModel.objects.get_or_create(financial_year=2018, financial_year_display='2018-19')
    obj, created = YearModel.objects.get_or_create(financial_year=2019, financial_year_display='2019-18')
    obj, created = YearModel.objects.get_or_create(financial_year=2020, financial_year_display='2020-20')


class Migration(migrations.Migration):
# Used to populate the FinancialYear and FinancialPeriod tables
    dependencies = [
        ('forecast', '0002_auto_20190206_1017'),
    ]

    operations = [
        migrations.RunPython(populate_year),
    ]