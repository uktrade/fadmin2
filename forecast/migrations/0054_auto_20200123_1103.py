# Generated by Django 2.2.8 on 2020-01-23 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0053_auto_20200123_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecasteditlock',
            name='locked_for_editing',
            field=models.BooleanField(default=False),
        ),
    ]