# Generated by Django 2.2.10 on 2020-04-15 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0042_auto_20200408_0837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simplehistoryditgroup',
            name='cost_centre',
        ),
        migrations.RemoveField(
            model_name='simplehistoryditgroup',
            name='directorate_code',
        ),
        migrations.RemoveField(
            model_name='simplehistoryditgroup',
            name='group_code',
        ),
        migrations.RemoveField(
            model_name='simplehistoryditgroup',
            name='history_user',
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='costcentre.CostCentre', verbose_name='DIT Cost Centre'),
        ),
        migrations.AlterField(
            model_name='simplehistorygiftandhospitality',
            name='group',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='costcentre.CostCentre', verbose_name='DIT Cost Centre'),
        ),
        migrations.DeleteModel(
            name='DITGroup',
        ),
        migrations.DeleteModel(
            name='SimpleHistoryDITGroup',
        ),
    ]