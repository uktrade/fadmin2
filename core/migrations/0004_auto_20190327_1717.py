# Generated by Django 2.1.5 on 2019-03-27 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0003_financialyear_in_use")]

    operations = [
        migrations.AlterField(
            model_name="admininfo",
            name="current_financial_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="core.FinancialYear"
            ),
        )
    ]