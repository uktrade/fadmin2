def can_view_gifthospitality(user):
    """Checks view permission, if the user can view gifthospitality
    they are allowed to view the section"""

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
    return False
