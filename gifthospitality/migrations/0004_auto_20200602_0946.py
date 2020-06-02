# Generated by Django 2.2.10 on 2020-06-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0003_auto_20200529_1046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftandhospitality',
            old_name='date_offered',
            new_name='date_received',
        ),
        migrations.AlterField(
            model_name='simplehistorygiftandhospitality',
            name='date_received',
            field=models.DateField(verbose_name='Date of event /  gift received'),
        ),
    ]