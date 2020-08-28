# Generated by Django 2.2.13 on 2020-08-28 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costcentre', '0003_auto_20200828_1053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='archivedcostcentre',
            options={'ordering': ['cost_centre_code'], 'verbose_name': 'Archived Cost Centre', 'verbose_name_plural': 'Archived Cost Centres'},
        ),
        migrations.AlterField(
            model_name='archivedcostcentre',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='costcentre_archivedcostcentre', to='core.FinancialYear'),
        ),
    ]
