# Generated by Django 2.1.2 on 2018-11-01 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('costcentre', '0008_auto_20181101_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costcentre',
            name='business_partner',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.PROTECT,
                                    to='costcentre.BusinessPartner',
                                    verbose_name='Finance Business Partner'),
        ),
    ]
