# Generated by Django 2.2 on 2019-08-07 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0012_create_oscar_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='ADIReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]