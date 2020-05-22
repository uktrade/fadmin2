# Generated by Django 2.1.2 on 2018-12-24 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("gifthospitality", "0024_remove_giftandhospitality_category")]

    operations = [
        migrations.AlterField(
            model_name="giftandhospitality",
            name="classification_fk",
            field=models.ForeignKey(
                default=1,
                limit_choices_to={"active": True},
                on_delete=django.db.models.deletion.PROTECT,
                to="gifthospitality.GiftAndHospitalityClassification",
                verbose_name="Type",
            ),
            preserve_default=False,
        )
    ]