# Generated by Django 3.0.3 on 2021-04-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0007_auto_20210325_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualuploadmonthlyfigure',
            name='oracle_amount',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='simplehistoryactualuploadmonthlyfigure',
            name='oracle_amount',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]