# Generated by Django 2.2.13 on 2020-08-20 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasurySS', '0003_auto_20200618_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplehistorysubsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('NON-BUDGET', 'NON-BUDGET'), ('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG'))), ('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
        migrations.AlterField(
            model_name='subsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('NON-BUDGET', 'NON-BUDGET'), ('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG'))), ('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
    ]
