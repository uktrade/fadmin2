# Generated by Django 2.2.10 on 2020-04-20 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0048_auto_20200416_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftandhospitality',
            name='days',
            field=models.CharField(default='default', max_length=200, verbose_name='Day'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='giftandhospitality',
            name='months',
            field=models.CharField(default='default', max_length=200, verbose_name='Month'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='giftandhospitality',
            name='years',
            field=models.CharField(default='default', max_length=200, verbose_name='Year'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='simplehistorygiftandhospitality',
            name='days',
            field=models.CharField(default='default', max_length=200, verbose_name='Day'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='simplehistorygiftandhospitality',
            name='months',
            field=models.CharField(default='default', max_length=200, verbose_name='Month'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='simplehistorygiftandhospitality',
            name='years',
            field=models.CharField(default='default', max_length=200, verbose_name='Year'),
            preserve_default=False,
        ),
    ]
