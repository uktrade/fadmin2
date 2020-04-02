# Generated by Django 2.2.10 on 2020-04-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasurySS', '0114_auto_20200402_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplehistorysubsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG'))), ('NON-BUDGET', 'NON-BUDGET'), ('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
        migrations.AlterField(
            model_name='subsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG'))), ('NON-BUDGET', 'NON-BUDGET'), ('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
    ]
