# Generated by Django 2.2 on 2019-06-21 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chartofaccountDIT', '0041_programmecode_budget_type_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmecode',
            name='budget_type_fk',
        ),
    ]
