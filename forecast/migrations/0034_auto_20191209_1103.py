# Generated by Django 2.2.4 on 2019-12-09 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0033_auto_20191209_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyfigure',
            name='financial_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='monthly_figures', to='forecast.FinancialCode'),
        ),
        migrations.AlterField(
            model_name='monthlyfigure',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]
