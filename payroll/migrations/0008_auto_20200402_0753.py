# Generated by Django 2.2.10 on 2020-04-02 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0007_auto_20200402_0752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ditgroup',
            options={'ordering': ['cost_centre'], 'verbose_name': 'DIT Group', 'verbose_name_plural': 'DIT Group'},
        ),
    ]
