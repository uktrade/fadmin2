# Generated by Django 2.2 on 2019-06-21 17:30

from django.db import migrations


def create_budget_types(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    BudgetType = apps.get_model("chartofaccountDIT", "BudgetType")
    BudgetType.objects.create(budget_type_key="DEL", budget_type="Programme DEL")
    BudgetType.objects.create(budget_type_key="AME", budget_type="Programme AME")
    BudgetType.objects.create(budget_type_key="ADMIN", budget_type="Admin")


class Migration(migrations.Migration):

    dependencies = [("chartofaccountDIT", "0045_programmecode_budget_type_fk")]

    operations = [migrations.RunPython(create_budget_types)]
