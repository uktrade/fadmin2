# Generated by Django 2.1.2 on 2018-11-28 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('gifthospitality', '0008_auto_20181128_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftandhospitality',
            name='category_fk',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='gifthospitality.GiftAndHospitalityCategory'),
        ),
        migrations.AddField(
            model_name='giftandhospitality',
            name='classification_fk',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='gifthospitality.GiftAndHospitalityClassification'),
        ),
        migrations.AddField(
            model_name='giftandhospitality',
            name='company_fk',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='gifthospitality.GiftAndHospitalityCompany'),
        ),
    ]