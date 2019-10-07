# Generated by Django 2.1.5 on 2019-04-09 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chartofaccountDIT', '0033_auto_20190403_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalfcomapping',
            name='financial_year',
        ),
        migrations.AlterModelOptions(
            name='historicalanalysis1',
            options={'ordering': ['financial_year', 'analysis1_code'], 'verbose_name': 'Historical Contract Reconciliation (Analysis 1)', 'verbose_name_plural': 'Historical Contract Reconciliations (Analysis 1)'},
        ),
        migrations.AlterModelOptions(
            name='historicalanalysis2',
            options={'ordering': ['financial_year', 'analysis2_code'], 'verbose_name': 'Historical Market (Analysis 2)', 'verbose_name_plural': 'Historical Markets (Analysis 2)'},
        ),
        migrations.AlterField(
            model_name='fcomapping',
            name='fco_code',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='FCO (Prism) Code'),
        ),
        migrations.AlterField(
            model_name='fcomapping',
            name='fco_description',
            field=models.CharField(max_length=300, verbose_name='FCO (Prism) Description'),
        ),
        migrations.DeleteModel(
            name='HistoricalFCOMapping',
        ),
    ]