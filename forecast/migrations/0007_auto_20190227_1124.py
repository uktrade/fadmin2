# Generated by Django 2.1.5 on 2019-02-27 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("forecast", "0006_auto_20190212_1222")]

    operations = [
        migrations.RemoveField(model_name="adireport", name="analysis1_code"),
        migrations.RemoveField(model_name="adireport", name="analysis2_code"),
        migrations.RemoveField(model_name="adireport", name="cost_centre"),
        migrations.RemoveField(model_name="adireport", name="natural_account_code"),
        migrations.RemoveField(model_name="adireport", name="programme"),
        migrations.DeleteModel(name="ADIReport"),
    ]
