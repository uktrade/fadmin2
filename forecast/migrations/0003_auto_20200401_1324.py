# Generated by Django 2.2.10 on 2020-04-01 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_create_financial_years'),
        ('end_of_month', '0001_initial'),
        ('forecast', '0003_auto_20200403_0828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simplehistoryarchivedforecastmonthlyfigure',
            name='financial_code',
        ),
        migrations.RemoveField(
            model_name='simplehistoryarchivedforecastmonthlyfigure',
            name='financial_period',
        ),
        migrations.RemoveField(
            model_name='simplehistoryarchivedforecastmonthlyfigure',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='simplehistoryarchivedforecastmonthlyfigure',
            name='forecast_month',
        ),
        migrations.RemoveField(
            model_name='simplehistoryarchivedforecastmonthlyfigure',
            name='forecast_year',
        ),
        migrations.RemoveField(
            model_name='simplehistoryarchivedforecastmonthlyfigure',
            name='history_user',
        ),
        migrations.AddField(
            model_name='actualuploadmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forecast_actualuploadmonthlyfigures', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AddField(
            model_name='budgetmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forecast_budgetmonthlyfigures', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AddField(
            model_name='budgetuploadmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forecast_budgetuploadmonthlyfigures', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AddField(
            model_name='forecastmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forecast_forecastmonthlyfigures', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AddField(
            model_name='simplehistoryactualuploadmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AddField(
            model_name='simplehistorybudgetmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AddField(
            model_name='simplehistorybudgetuploadmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AddField(
            model_name='simplehistoryforecastmonthlyfigure',
            name='archived_status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='end_of_month.EndOfMonthStatus'),
        ),
        migrations.AlterUniqueTogether(
            name='actualuploadmonthlyfigure',
            unique_together={('financial_code', 'financial_year', 'financial_period', 'archived_status')},
        ),
        migrations.AlterUniqueTogether(
            name='budgetmonthlyfigure',
            unique_together={('financial_code', 'financial_year', 'financial_period', 'archived_status')},
        ),
        migrations.AlterUniqueTogether(
            name='budgetuploadmonthlyfigure',
            unique_together={('financial_code', 'financial_year', 'financial_period', 'archived_status')},
        ),
        migrations.AlterUniqueTogether(
            name='forecastmonthlyfigure',
            unique_together={('financial_code', 'financial_year', 'financial_period', 'archived_status')},
        ),
        migrations.DeleteModel(
            name='ArchivedForecastMonthlyFigure',
        ),
        migrations.DeleteModel(
            name='SimpleHistoryArchivedForecastMonthlyFigure',
        ),
    ]
