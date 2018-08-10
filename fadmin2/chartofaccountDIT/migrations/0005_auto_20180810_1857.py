# Generated by Django 2.0.2 on 2018-08-10 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chartofaccountDIT', '0004_auto_20180719_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nacdashboardgrouping',
            name='linked_budget_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='chartofaccountDIT.NaturalCode', verbose_name='Budget Code'),
        ),
        migrations.AlterField(
            model_name='naturalcode',
            name='dashboard_grouping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='chartofaccountDIT.NACDashboardGrouping', verbose_name='Budget Category'),
        ),
    ]
