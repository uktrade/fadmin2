# Generated by Django 2.2.13 on 2020-08-19 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treasuryCOA', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicl5account',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='treasurycoa_historicl5account_financial_year', to='core.FinancialYear'),
        ),
    ]
