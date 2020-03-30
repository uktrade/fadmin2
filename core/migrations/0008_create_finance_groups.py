from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.db import migrations


def add_all_permissions():
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None


def create_groups(apps, schema_editor):
    add_all_permissions()

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    finance_business_partners, _ = Group.objects.get_or_create(
        name='Finance Business Partner/BSCE',

    )
    assign_edit_for_own_cost_centres = Permission.objects.get(
        codename='assign_edit_for_own_cost_centres',
    )
    finance_business_partners.permissions.add(
        assign_edit_for_own_cost_centres,
    )

    can_edit_whilst_closed = Permission.objects.get(
        codename='can_edit_whilst_closed',
    )
    finance_business_partners.permissions.add(
        can_edit_whilst_closed,
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
        ("core", "0007_create_financial_years"),
        ("costcentre", "0033_auto_20200327_0931"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
