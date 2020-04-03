# Generated by Django 2.2.10 on 2020-03-27 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costcentre', '0032_auto_20200326_1653'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='costcentre',
            options={'default_permissions': ('change',), 'ordering': ['cost_centre_code'], 'permissions': (
                ('edit_forecast_all_cost_centres', 'Edit all cost centres'),
                (
                    'assign_edit_for_own_cost_centres',
                    'Assign edit cost centre for own cost centres',
                ),
            ), 'verbose_name': 'Cost Centre', 'verbose_name_plural': 'Cost Centres'},
        ),
    ]
