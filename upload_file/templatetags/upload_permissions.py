from django import template

from upload_file.models import UploadPermission

register = template.Library()


@register.simple_tag
def has_actuals_upload_permission(user):
    upload_permissions = UploadPermission.objects.filter(
        user=user,
    ).first()

    if upload_permissions is not None and upload_permissions.upload_actuals:
        return True

    return False


@register.simple_tag
def has_budget_upload_permission(user):
    upload_permissions = UploadPermission.objects.filter(
        user=user,
    ).first()

    if upload_permissions is not None and upload_permissions.upload_budget:
        return True

    return False
