# Generated by Django 2.2.13 on 2020-08-28 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chartofaccountDIT', '0004_auto_20200820_0751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archivednaturalcode',
            old_name='expenditure_category',
            new_name='expenditure_category_description',
        ),
        migrations.RenameField(
            model_name='simplehistoryarchivednaturalcode',
            old_name='expenditure_category',
            new_name='expenditure_category_description',
        ),
    ]
