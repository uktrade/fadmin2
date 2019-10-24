# Generated by Django 2.1.5 on 2019-04-09 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_financialyear_current_year"),
        ("chartofaccountDIT", "0034_auto_20190409_1542"),
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
                    models.CharField(
                        max_length=300, verbose_name="FCO (Prism) Description"
                    ),
                ),
                ("fco_code", models.IntegerField(verbose_name="FCO (Prism) Code")),
                (
                    "account_L6_code",
                    models.IntegerField(verbose_name="Oracle (DIT) Code"),
                ),
                (
                    "account_L6_description",
                    models.CharField(
                        max_length=200, verbose_name="Oracle (DIT) Description"
                    ),
                ),
                (
                    "nac_category_description",
                    models.CharField(max_length=200, verbose_name="Budget Grouping"),
                ),
                (
                    "budget_description",
                    models.CharField(max_length=200, verbose_name="Budget Category"),
                ),
                (
                    "economic_budget_code",
                    models.CharField(max_length=200, verbose_name="Expenditure Type"),
                ),
                ("active", models.BooleanField(default=False)),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.FinancialYear",
                    ),
                ),
            ],
            options={
                "verbose_name": "Historic FCO Mapping",
                "verbose_name_plural": "Historic FCO Mappings",
                "ordering": ["financial_year", "fco_code"],
            },
        )
    ]
