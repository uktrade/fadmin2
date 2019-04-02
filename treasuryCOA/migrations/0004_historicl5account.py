# Generated by Django 2.1.5 on 2019-04-02 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_financialyear_current_year'),
        ('treasuryCOA', '0003_auto_20190402_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricL5Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.DateTimeField(auto_now_add=True)),
                ('account_l5_long_name', models.CharField(blank=True, max_length=255, verbose_name='account l5 long name')),
                ('account_l5_description', models.CharField(blank=True, max_length=2048, verbose_name='account l5 description')),
                ('economic_budget_code', models.CharField(blank=True, max_length=255, verbose_name='economic budget code')),
                ('sector_code', models.CharField(blank=True, max_length=255, verbose_name='sector code')),
                ('estimates_column_code', models.CharField(choices=[('GROSS', 'GROSS'), ('INCOME', 'INCOME'), ('N/A', 'N/A')], default='N/A', max_length=25, verbose_name='estimates column code')),
                ('usage_code', models.CharField(blank=True, choices=[('BOTH', 'BOTH'), ('OUTTURN', 'OUTTURN'), ('PLANS', 'PLANS')], default='BOTH', max_length=25, verbose_name='usage code')),
                ('cash_indicator_code', models.CharField(blank=True, max_length=5, verbose_name='cash indicator code')),
                ('account_l5_code', models.BigIntegerField(verbose_name='account l5 code')),
                ('account_l4_code', models.BigIntegerField(verbose_name='account l4 code')),
                ('account_l4_long_name', models.CharField(blank=True, max_length=255, verbose_name='account l4 long name')),
                ('account_l3_code', models.BigIntegerField(verbose_name='account l3 code')),
                ('account_l3_long_name', models.CharField(blank=True, max_length=255, verbose_name='account l3 long name')),
                ('account_l2_code', models.BigIntegerField(verbose_name='account l2 code')),
                ('account_l2_long_name', models.CharField(blank=True, max_length=255, verbose_name='account l2 long name')),
                ('account_l1_code', models.BigIntegerField(verbose_name='account l1 code')),
                ('account_l1_long_name', models.CharField(blank=True, max_length=255, verbose_name='account l1 long name')),
                ('account_code', models.CharField(blank=True, max_length=255, verbose_name='accounts code')),
                ('account_l0_code', models.CharField(max_length=255, verbose_name='account l0 code')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.FinancialYear')),
            ],
            options={
                'verbose_name': 'Archived Treasury Level 5 COA',
            },
        ),
    ]
