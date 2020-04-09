# Generated by Django 2.1.2 on 2018-11-01 16:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("costcentre", "0006_costcentre_bsce_email")]

    operations = [
        migrations.CreateModel(
            name="BusinessPartner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("active", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(max_length=300)),
                (
                    "bp_email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        verbose_name="Business Partner email",
                    ),
                ),
            ],
            options={
                "verbose_name": "Business Partner",
                "verbose_name_plural": "Business Partners",
            },
        )
    ]
