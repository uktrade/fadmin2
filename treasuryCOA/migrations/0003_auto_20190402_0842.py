# Generated by Django 2.1.5 on 2019-04-02 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treasuryCOA', '0002_historicl5account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicl5account',
            name='account_l4',
        ),
        migrations.DeleteModel(
            name='HistoricL5Account',
        ),
    ]
