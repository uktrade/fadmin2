# Generated by Django 2.0.2 on 2018-07-12 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treasuryCOA', '0003_auto_20180712_1430'),
    ]

    operations = [
        migrations.RenameField(
            model_name='l5account',
            old_name='account_l5Description',
            new_name='account_l5_description',
        ),
    ]
