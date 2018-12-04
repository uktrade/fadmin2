# Generated by Django 2.1.2 on 2018-12-03 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0009_auto_20181128_1416'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='giftandhospitalitycategory',
            options={'ordering': ['gif_hospitality_category'], 'verbose_name': 'Gift and Hospitality Category', 'verbose_name_plural': 'Gift and Hospitality Categories'},
        ),
        migrations.AlterModelOptions(
            name='giftandhospitalityclassification',
            options={'ordering': ['gif_hospitality_classification'], 'verbose_name': 'Gift and Hospitality Classification', 'verbose_name_plural': 'Gift and Hospitality Classifications'},
        ),
        migrations.AlterModelOptions(
            name='giftandhospitalitycompany',
            options={'ordering': ['gif_hospitality_company'], 'verbose_name': 'Gift and Hospitality Company', 'verbose_name_plural': 'Gift and Hospitality Companies'},
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='category_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gifthospitality.GiftAndHospitalityCategory', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='classification',
            field=models.CharField(max_length=100, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='classification_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gifthospitality.GiftAndHospitalityClassification', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='company',
            field=models.CharField(max_length=100, verbose_name='Company received from'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='company_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gifthospitality.GiftAndHospitalityCompany', verbose_name='company'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='company_rep',
            field=models.CharField(max_length=50, verbose_name='Company Representative received from'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='date_offered',
            field=models.DateField(verbose_name='Date of event / Date gift offered'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='offer',
            field=models.CharField(choices=[('Received', 'Received by DIT Staff'), ('Offered', 'Given by DIT Staff')], max_length=50, verbose_name='Hospitality/Gift was'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='reason',
            field=models.CharField(max_length=1000, verbose_name='Reason for hospitality'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='rep',
            field=models.CharField(max_length=255, verbose_name='DIT Representative offered to'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Estimated value of offer (£)'),
        ),
    ]
