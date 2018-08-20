# Generated by Django 2.0.2 on 2018-08-16 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasurySS', '0008_auto_20180810_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('NON-BUDGET', 'NON-BUDGET'), ('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG'))), ('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
    ]
