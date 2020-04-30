from datetime import date

from guardian.shortcuts import (
    get_objects_for_user as guardian_get_objects_for_user,
)

from gifthospitality.models import (
    GiftAndHospitality,
    GiftHospitalityPermissions,
)


def can_view_gifthospitality(user):
    """Checks view permission, if the user can edit ANY
    cost centre, they are allowed to view ALL forecasts"""
    if can_view_gifthospitality(
        user
    ):
        return True

    return user.has_perm(
        "gifthospitality.can_view_gifthospitality"
    )


def user_in_group(user, group):
    return user.groups.filter(
        name=group,
    ).exists()


def can_all_gifthospitality_be_viewed(user):
    if user.is_superuser:
        return True

    if user.has_perm("gifthospitality.can_view_all_gifthospitality"):
        return True