# Generated by Django 2.2 on 2019-06-19 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('treasurySS', '0090_auto_20190619_0956'),
        ('costcentre', '0024_costcentre_used_for_travel'),
    ]

    # operations = [
    #     migrations.AddField(
    #         model_name='costcentre',
    #         name='subsegment_mapping',
    #         field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='treasurySS.DITSSGroup', verbose_name='Sub Segment Group Mapping'),
    #     ),
    # ]