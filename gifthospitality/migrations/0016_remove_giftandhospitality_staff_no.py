# Generated by Django 2.1.2 on 2018-12-12 09:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gifthospitality', '0015_auto_20181211_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftandhospitality',
            name='staff_no',
        ),
    ]