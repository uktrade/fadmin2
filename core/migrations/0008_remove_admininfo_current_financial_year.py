# Generated by Django 2.2 on 2019-07-08 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("core", "0007_auto_20190708_0719")]

    operations = [
        migrations.RemoveField(model_name="admininfo", name="current_financial_year")
    ]
