# Generated by Django 2.0.2 on 2018-08-29 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasuryCOA', '0002_auto_20180828_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='l1account',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='l2account',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='l3account',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='l4account',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='l5account',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
