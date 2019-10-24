# Generated by Django 2.1.5 on 2019-04-03 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("treasurySS", "0078_auto_20190403_0957")]

    operations = [
        migrations.AlterField(
            model_name="subsegment",
            name="control_budget_detail_code",
            field=models.CharField(
                choices=[
                    ("DEL", (("DEL ADMIN", "DEL ADMIN"), ("DEL PROG", "DEL PROG"))),
                    ("NON-BUDGET", "NON-BUDGET"),
                    (
                        "AME",
                        (("DEPT AME", "DEPT AME"), ("NON-DEPT AME", "NON-DEPT AME")),
                    ),
                ],
                default="NON-BUDGET",
                max_length=50,
                verbose_name="control budget detail code",
            ),
        )
    ]
