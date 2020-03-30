from datetime import datetime

from guardian.shortcuts import (
    get_objects_for_user as guardian_get_objects_for_user,
)

from forecast.models import (
    ForecastEditOpenState,
    UnlockedForecastEditors,
)


def can_view_forecasts(user):
    # If user can edit ANY cost centre, they
    # are allowed to view ALL forecasts
    if can_edit_at_least_one_cost_centre(
        user
    ):
        return True

    return user.has_perm(
        "forecast.can_view_forecasts"
    )


def is_system_locked():
    today = datetime.now()
    forecast_edit_date = ForecastEditOpenState.objects.get()

    if (
        forecast_edit_date.lock_date and
        forecast_edit_date.lock_date.month == today.month and
        forecast_edit_date.lock_date.year == today.year
    ):
        return True

    return False


def is_system_closed():
    forecast_edit_date = ForecastEditOpenState.objects.get()

    if forecast_edit_date.closed:
        return True

    return False


def user_in_group(user, group):
    return user.groups.filter(
        name=group,
    ).exists()


def can_forecast_be_edited(user):
    if user.is_superuser:
        return True

    closed = is_system_closed()
    locked = is_system_locked()

    if not closed and not locked:
        return True

    if user.has_perm("forecast.can_edit_whilst_locked"):
        return True

    if closed and not locked and user.has_perm("forecast.can_edit_whilst_closed"):
        return True

    if UnlockedForecastEditors.objects.filter(
        user=user,
    ).exists():
        return True

    return False


def can_edit_at_least_one_cost_centre(user):
    cost_centres = guardian_get_objects_for_user(
        user,
        "costcentre.change_costcentre",
    )

    return cost_centres.count() > 0


def can_edit_cost_centre(user, cost_centre_code):
    return user.has_perm(
        "costcentre.change_costcentre",
        cost_centre_code,
    )
