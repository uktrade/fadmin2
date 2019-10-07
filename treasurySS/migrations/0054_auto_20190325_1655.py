# Generated by Django 2.1.5 on 2019-03-25 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasurySS', '0053_auto_20190325_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME'))), ('NON-BUDGET', 'NON-BUDGET'), ('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
    ]