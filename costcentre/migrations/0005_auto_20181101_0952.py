# Generated by Django 2.1.2 on 2018-11-01 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('costcentre', '0004_bsceemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bsceemail',
            name='bsce_email',
            field=models.EmailField(max_length=254, verbose_name='BSCE email'),
        ),
    ]
