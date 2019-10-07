# Generated by Django 2.2.4 on 2019-08-14 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasurySS', '0114_auto_20190807_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG'))), ('NON-BUDGET', 'NON-BUDGET'), ('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME')))], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
    ]