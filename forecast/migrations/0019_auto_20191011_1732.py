# Generated by Django 2.2.4 on 2019-10-11 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chartofaccountDIT", "0049_auto_20191003_1317"),
        ("forecast", "0018_forecast_expenditure_type"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Forecast_Expenditure_Type", new_name="ForecastExpenditureType"
        )
    ]
