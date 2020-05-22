# Generated by Django 2.2.10 on 2020-04-16 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0047_auto_20200416_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftandhospitality',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gifthospitality.Grade', verbose_name='grade'),
        ),
        migrations.AlterField(
            model_name='simplehistorygiftandhospitality',
            name='grade',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gifthospitality.Grade', verbose_name='grade'),
        ),
    ]