# Generated by Django 2.0.2 on 2018-08-28 09:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subsegmentuktimapping',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subsegmentuktimapping',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
