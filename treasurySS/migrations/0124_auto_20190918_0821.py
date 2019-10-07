# Generated by Django 2.2.4 on 2019-09-18 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasurySS', '0123_auto_20190918_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsegment',
            name='control_budget_detail_code',
            field=models.CharField(choices=[('AME', (('DEPT AME', 'DEPT AME'), ('NON-DEPT AME', 'NON-DEPT AME'))), ('DEL', (('DEL ADMIN', 'DEL ADMIN'), ('DEL PROG', 'DEL PROG'))), ('NON-BUDGET', 'NON-BUDGET')], default='NON-BUDGET', max_length=50, verbose_name='control budget detail code'),
        ),
    ]