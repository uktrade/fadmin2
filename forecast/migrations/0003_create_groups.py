from django.contrib.auth.models import (
    Group,
    Permission,
)

from django.db import migrations


def create_groups(apps, schema_editor):
    finance_business_partners, _ = Group.objects.get_or_create(
        name='Finance Business Partner/BSCE',

    )
    assign_edit_for_own_cost_centres = Permission.objects.get(
        codename='assign_edit_for_own_cost_centres',
    )
    finance_business_partners.permissions.add(
        assign_edit_for_own_cost_centres,
    )

    finance_adminstrators, _ = Group.objects.get_or_create(
        name='Finance Administrator',
    )
    edit_all_cost_centres = Permission.objects.get(
        codename='edit_forecast_all_cost_centres',
    )
    finance_adminstrators.permissions.add(
        edit_all_cost_centres,
    )
    # Add permission on edit lock
    permission_codenames = [
        "can_set_edit_lock",
        "can_edit_whilst_locked",
        "can_unlock_user",
    ]

    # Permission on unlocked user lists
    for permission_codename in permission_codenames:
        permission = Permission.objects.get(
            codename=permission_codename,
        )
        finance_adminstrators.permissions.add(
            permission,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("forecast", "0002_populate_models"),
        ("costcentre", "0033_auto_20200327_0931"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
