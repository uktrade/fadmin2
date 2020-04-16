# Generated by Django 2.2.10 on 2020-04-02 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0032_auto_20200402_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftandhospitality',
            name='grade_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='payroll.Grade', verbose_name='grade'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='group_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='simplehistorygiftandhospitality',
            name='group_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Group'),
        ),
    ]
