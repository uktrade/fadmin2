# Generated by Django 2.2.10 on 2020-03-26 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costcentre', '0030_auto_20200214_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='costcentre',
            options={'ordering': ['cost_centre_code'], 'permissions': (('edit_forecast', 'Edit cost centre forecast'),), 'verbose_name': 'Cost Centre', 'verbose_name_plural': 'Cost Centres'},
        ),
    ]
