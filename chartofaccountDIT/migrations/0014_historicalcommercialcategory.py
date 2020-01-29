# Generated by Django 2.1.5 on 2019-04-02 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_financialyear_current_year"),
        ("chartofaccountDIT", "0013_historicalanalysis1_historicalanalysis2"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricCommercialCategory",
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
                    "commercial_category",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Commercial Category"
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=5000, null=True),
                ),
                ("approvers", models.CharField(blank=True, max_length=5000, null=True)),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.FinancialYear",
                    ),
                ),
            ],
            options={
                "verbose_name": "Historic Commercial Category",
                "verbose_name_plural": "Historic Commercial Categories",
                "ordering": ["financial_year", "commercial_category"],
            },
        )
    ]
