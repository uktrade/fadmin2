# Generated by Django 2.1.2 on 2018-11-08 17:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("chartofaccountDIT", "0005_auto_20181105_1135")]

    operations = [
        migrations.AlterModelOptions(
            name="interentityl1",
            options={
                "verbose_name": "Government Body",
                "verbose_name_plural": "Government Bodies",
            },
        ),
        migrations.AlterField(
            model_name="interentity",
            name="cpid",
            field=models.CharField(
                max_length=10, verbose_name="Treasury - CPID (Departmental Code No.)"
            ),
        ),
        migrations.AlterField(
            model_name="interentity",
            name="l2_description",
            field=models.CharField(
                max_length=100, verbose_name="ORACLE - Inter Entity Description"
            ),
        ),
        migrations.AlterField(
            model_name="interentity",
            name="l2_value",
            field=models.CharField(
                max_length=10,
                primary_key=True,
                serialize=False,
                verbose_name="ORACLE - Inter Entity Code",
            ),
        ),
        migrations.AlterField(
            model_name="interentityl1",
            name="l1_description",
            field=models.CharField(
                max_length=100, verbose_name="Government Body Description"
            ),
        ),
        migrations.AlterField(
            model_name="interentityl1",
            name="l1_value",
            field=models.CharField(
                max_length=10,
                primary_key=True,
                serialize=False,
                verbose_name="Government Body",
            ),
        ),
    ]
