# Generated by Django 2.2.10 on 2020-04-02 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0030_auto_20200402_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftandhospitality',
            name='rep_fk',
            field=models.CharField(blank=True, default='Unspecified', max_length=200, verbose_name='DIT representative offered to/from'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='simplehistorygiftandhospitality',
            name='rep_fk',
            field=models.CharField(blank=True, default='Unspecified', max_length=200, verbose_name='DIT representative offered to/from'),
            preserve_default=False,
        ),
    ]
