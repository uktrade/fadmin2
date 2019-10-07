# Generated by Django 2.1.2 on 2018-12-03 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('gifthospitality', '0012_auto_20181203_1729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='giftandhospitality',
            options={'ordering': ['-id'], 'verbose_name': 'Gift and Hospitality',
                     'verbose_name_plural': 'Gift and Hospitality'},
        ),
        migrations.AlterModelOptions(
            name='giftandhospitalityclassification',
            options={'ordering': ['sequence_no'], 'verbose_name': 'Gift and Hospitality Type',
                     'verbose_name_plural': 'Gift and Hospitality Types'},
        ),
        migrations.AddField(
            model_name='giftandhospitality',
            name='gift_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='category_fk',
            field=models.ForeignKey(blank=True, limit_choices_to={'active': True}, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='gifthospitality.GiftAndHospitalityCategory',
                                    verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='classification_fk',
            field=models.ForeignKey(blank=True, limit_choices_to={'active': True}, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='gifthospitality.GiftAndHospitalityClassification',
                                    verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='company_fk',
            field=models.ForeignKey(blank=True, limit_choices_to={'active': True}, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='gifthospitality.GiftAndHospitalityCompany',
                                    verbose_name='company'),
        ),
    ]