# Generated by Django 2.1.2 on 2018-11-08 17:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("costcentre", "0012_costcentre_disabled_with_actual")]

    operations = [
        migrations.AlterModelOptions(
            name="costcentreperson",
            options={
                "ordering": ["surname", "name"],
                "verbose_name": "Hierarchy Responsibility",
                "verbose_name_plural": "Hierarchy Responsibilities",
            },
        )
    ]
