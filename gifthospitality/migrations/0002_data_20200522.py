from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.db import migrations, models

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


def create_gift_hospitality_groups(apps, schema_editor):
    add_all_permissions()

    # Gift and Hospitality Admin
    gift_hospitality_admin, _ = Group.objects.get_or_create(
        name='Gift and Hospitality Admin',
    )


class Migration(migrations.Migration):
    dependencies = [
        ("gifthospitality", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_gift_hospitality_groups),

        migrations.AddField(
            model_name='giftandhospitality',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Other company'),
        ),
        migrations.AddField(
            model_name='simplehistorygiftandhospitality',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Other company'),
        ),

        migrations.AlterField(
            model_name='giftandhospitality',
            name='date_agreed',
            field=models.DateField(verbose_name='Date of event /  gift received'),
        ),
        migrations.AlterField(
            model_name='simplehistorygiftandhospitality',
            name='date_agreed',
            field=models.DateField(verbose_name='Date of event /  gift received'),
        ),
    ]
