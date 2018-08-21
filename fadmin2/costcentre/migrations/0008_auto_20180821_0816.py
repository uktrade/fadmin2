# Generated by Django 2.0.2 on 2018-08-21 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costcentre', '0007_auto_20180820_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costcentre',
            name='business_partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='business_partner', to='payroll.DITPeople', verbose_name='Finance Business Partner'),
        ),
        migrations.AlterField(
            model_name='departmentalgroup',
            name='director_general',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payroll.DITPeople'),
        ),
    ]
