from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.db import migrations

Permission = apps.get_model('auth', 'Permission')
Group = apps.get_model('auth', 'Group')


def add_all_permissions():
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None


def assign_permissions(group, permission_codenames):
    for permission_codename in permission_codenames:
        permission = Permission.objects.get(
            codename=permission_codename,
        )
        group.permissions.add(
            permission,
        )


def create_groups(apps, schema_editor):
    add_all_permissions()

    # Finance Business Partners
    finance_business_partners, _ = Group.objects.get_or_create(
        name='Finance Business Partner/BSCE',

    )

    assign_permissions(
        finance_business_partners, [
            "can_edit_whilst_closed",
            "assign_edit_for_own_cost_centres",
            "change_costcentre",  # admin permission
        ],
    )

    # Finance admins
    finance_adminstrators, _ = Group.objects.get_or_create(
        name='Finance Administrator',
    )

    assign_permissions(
        finance_adminstrators, [
            "edit_forecast_all_cost_centres",
            "can_allow_user_to_edit_cost_centre",
            "assign_user_to_cost_centre",
            "can_set_edit_lock",
            "can_edit_whilst_locked",
            "change_costcentre",  # admin permission
            "change_user",  # admin permission
            "add_unlockedforecasteditors",  # admin permission
            "delete_unlockedforecasteditors",  # admin permission
            "view_unlockedforecasteditors",  # admin permission
        ],
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_create_financial_years"),
        ("forecast", "0005_auto_20200330_1043"),
        ("costcentre", "0033_auto_20200327_0931"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
