# Generated by Django 2.1.5 on 2019-04-03 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("chartofaccountDIT", "0026_historicalfcomapping")]

    operations = [
        migrations.RemoveField(model_name="historicalanalysis2", name="financial_year"),
        migrations.DeleteModel(name="HistoricalAnalysis2"),
    ]
