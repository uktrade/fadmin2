from django import template

<<<<<<< HEAD
from forecast.models import ForecastPermission
=======
from upload_file.models import UploadPermission
>>>>>>> dev

register = template.Library()


@register.simple_tag
def has_upload_permission(user):
<<<<<<< HEAD
    forecast_permission = ForecastPermission.objects.filter(
        user=user,
    ).first()

    if forecast_permission and forecast_permission.can_upload:
=======
    upload_permissions = UploadPermission.objects.filter(
        user=user,
    ).first()

    if upload_permissions is not None:
>>>>>>> dev
        return True

    return False
