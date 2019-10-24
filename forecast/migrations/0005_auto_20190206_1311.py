# Generated by Django 2.1.5 on 2019-02-06 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("forecast", "0004_auto_20190206_1129")]

    operations = [
        migrations.AlterModelOptions(
            name="financialperiod", options={"ordering": ["financial_period_code"]}
        ),
        migrations.AlterField(
            model_name="budget",
            name="analysis1_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.Analysis1",
            ),
        ),
        migrations.AlterField(
            model_name="budget",
            name="analysis2_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.Analysis2",
            ),
        ),
        migrations.AlterField(
            model_name="budget",
            name="project_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.ProjectCode",
            ),
        ),
        migrations.AlterField(
            model_name="monthlyfigure",
            name="analysis1_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.Analysis1",
            ),
        ),
        migrations.AlterField(
            model_name="monthlyfigure",
            name="analysis2_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.Analysis2",
            ),
        ),
        migrations.AlterField(
            model_name="monthlyfigure",
            name="project_code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.ProjectCode",
            ),
        ),
    ]
