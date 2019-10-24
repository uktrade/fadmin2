# Generated by Django 2.1.5 on 2019-02-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("forecast", "0007_auto_20190227_1124")]

    operations = [
        migrations.AddField(
            model_name="financialperiod",
            name="actual_loaded",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="financialperiod",
            name="period_short_name",
            field=models.CharField(max_length=10),
        ),
    ]
