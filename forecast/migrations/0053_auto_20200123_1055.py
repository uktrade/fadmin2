# Generated by Django 2.2.8 on 2020-01-23 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0052_auto_20200117_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastEditLock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locked_for_editing', models.BooleanField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='budgetmonthlyfigure',
            managers=[
            ],
        ),
    ]
