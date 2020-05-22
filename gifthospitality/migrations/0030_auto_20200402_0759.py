# Generated by Django 2.2.10 on 2020-04-02 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0008_auto_20200402_0753'),
        ('gifthospitality', '0029_auto_20200214_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftandhospitality',
            name='group_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payroll.DITGroup', verbose_name='DIT Group'),
        ),
        migrations.AddField(
            model_name='simplehistorygiftandhospitality',
            name='group_fk',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='payroll.DITGroup', verbose_name='DIT Group'),
        ),
    ]