# Generated by Django 2.1.5 on 2019-04-03 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_financialyear_current_year"),
        ("chartofaccountDIT", "0025_auto_20190403_0957"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalFCOMapping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("archived", models.DateTimeField(auto_now_add=True)),
                (
                    "fco_description",
                    models.CharField(max_length=300, verbose_name="FCO Description"),
                ),
                ("fco_code", models.IntegerField(verbose_name="FCO Code")),
                ("account_L6_code", models.IntegerField(verbose_name="Oracle Code")),
                (
                    "account_L6_description",
                    models.CharField(max_length=200, verbose_name="Oracle Description"),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.FinancialYear",
                    ),
                ),
            ],
            options={
                "verbose_name": "Historical FCO Mapping",
                "verbose_name_plural": "Historical FCO Mappings",
                "ordering": ["financial_year", "fco_code"],
            },
        )
    ]
