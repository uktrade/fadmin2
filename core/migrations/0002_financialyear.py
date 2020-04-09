# Generated by Django 2.1.5 on 2019-03-25 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="FinancialYear",
            fields=[
                (
                    "financial_year",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("financial_year_display", models.CharField(max_length=20)),
                ("current_year", models.BooleanField(default=False)),
            ],
        )
    ]
