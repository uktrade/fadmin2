# Generated by Django 2.2.4 on 2019-11-28 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0035_auto_20191128_1151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budget',
            old_name='budget',
            new_name='amount',
        ),
    ]