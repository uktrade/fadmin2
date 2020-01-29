# Generated by Django 2.1.5 on 2019-04-10 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("chartofaccountDIT", "0035_historicalfcomapping")]

    operations = [
        migrations.AlterField(
            model_name="historicfcomapping",
            name="budget_description",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Budget Category"
            ),
        ),
        migrations.AlterField(
            model_name="historicfcomapping",
            name="nac_category_description",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Budget Grouping"
            ),
        ),
    ]
