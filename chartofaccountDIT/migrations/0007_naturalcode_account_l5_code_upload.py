# Generated by Django 2.1.2 on 2018-11-14 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('treasuryCOA', '0001_initial'),
        ('chartofaccountDIT', '0006_auto_20181109_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturalcode',
            name='account_L5_code_upload',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.PROTECT,
                                    related_name='L5_OSCAR_Upload', to='treasuryCOA.L5Account',
                                    verbose_name='L5 for OSCAR upload'),
        ),
    ]
