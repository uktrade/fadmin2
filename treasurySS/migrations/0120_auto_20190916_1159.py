# Generated by Django 2.2.4 on 2019-09-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("treasurySS", "0119_auto_20190912_1430")]

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
