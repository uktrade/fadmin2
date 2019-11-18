# Generated by Django 2.2.4 on 2019-10-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasurySS', '0134_auto_20191023_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME'))), ('NON-BUDGET', 'NON-BUDGET'), ('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
    ]
