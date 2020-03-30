# Generated by Django 2.2.10 on 2020-03-30 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0004_auto_20200327_0931'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forecasteditopenstate',
            options={'default_permissions': ('',), 'permissions': [('can_set_edit_lock', 'Can set edit lock'), ('can_edit_whilst_closed', 'Can edit forecasts whilst system is closed'), ('can_edit_whilst_locked', 'Can edit forecasts whilst system is locked')]},
        ),
        migrations.AlterModelOptions(
            name='unlockedforecasteditors',
            options={'default_permissions': ('',), 'permissions': [('can_unlock_user', 'Can unlock a user')]},
        ),
        migrations.RemoveField(
            model_name='forecasteditopenstate',
            name='locked',
        ),
        migrations.RemoveField(
            model_name='simplehistoryforecasteditopenstate',
            name='locked',
        ),
        migrations.AddField(
            model_name='forecasteditopenstate',
            name='lock_date',
            field=models.DateField(help_text="If the lock date is set, after this date the system will remain locked for the remainder of the date's month", null=True),
        ),
        migrations.AddField(
            model_name='simplehistoryforecasteditopenstate',
            name='lock_date',
            field=models.DateField(help_text="If the lock date is set, after this date the system will remain locked for the remainder of the date's month", null=True),
        ),
    ]
