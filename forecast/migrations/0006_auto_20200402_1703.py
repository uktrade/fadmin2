# Generated by Django 2.2.10 on 2020-04-02 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0004_auto_20200401_1332'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='actualuploadmonthlyfigure',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='budgetmonthlyfigure',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='budgetuploadmonthlyfigure',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='forecastmonthlyfigure',
            unique_together=set(),
        ),
    ]
