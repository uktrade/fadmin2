# Generated by Django 2.1.2 on 2018-12-17 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0018_auto_20181212_1114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='giftandhospitality',
            options={'ordering': ['-id'], 'verbose_name': 'Gift and Hospitality', 'verbose_name_plural': 'Gift and Hospitality'},
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='action_taken',
            field=models.CharField(blank=True, choices=[('Action1', 'Refused'), ('Action2', 'Accepted (difference paid to Department)'), ('Action3', 'Accepted (surrendered to Department)'), ('Action0', 'Accepted')], max_length=200, verbose_name='Action taken'),
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='entered_date_stamp',
            field=models.DateField(verbose_name='Date entered'),
        ),
    ]
