from datetime import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from guardian.shortcuts import (
    get_objects_for_user as guardian_get_objects_for_user,
)

from forecast.models import (
    ForecastEditOpenState,
    UnlockedForecastEditors,
)


class NoCostCentreCodeInURLError(Exception):
    pass


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


def can_edit_forecast(user):
    if user.is_superuser:
        return True

    closed = is_system_closed()
    locked = is_system_locked()

    if not closed and not locked:
        return True

    if user_in_group(
        user,
        "Finance Administrator",
    ):
        return True

    # Finance Business Partners can edit when
    # system is closed but not locked
    if user_in_group(
        user,
        "Finance Business Partner/BSCE",
    ) and not locked:
        return True

    if UnlockedForecastEditors.objects.filter(
        user=user,
    ).exists():
        return True

    return False


def has_edit_permission(user, cost_centre_code):
    cost_centres = guardian_get_objects_for_user(
        user,
        "costcentre.change_costcentre",
    )

    # If user has permission on
    # one or more CCs then let them view
    return cost_centres.count() > 0


class ForecastViewPermissionMixin(UserPassesTestMixin):
    cost_centre_code = None

    def test_func(self):
        # Users with permission to edit ANY
        # cost centre can view forecasts
        cost_centres = guardian_get_objects_for_user(
            self.request.user,
            "costcentre.change_costcentre",
        )

        # If user has permission on
        # one or more CCs then let them view
        if cost_centres.count() > 0:
            return True

        return self.request.user.has_perm(
            "forecast.can_view_forecasts"
        )

    def handle_no_permission(self):
        return redirect(
            reverse(
                "index",
            )
        )


class CostCentrePermissionTest(UserPassesTestMixin):
    cost_centre_code = None
    edit_not_available = False

    def test_func(self):
        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs['cost_centre_code']

        has_permission = has_edit_permission(
            self.request.user,
            self.cost_centre_code,
        )

        can_edit = can_edit_forecast(self.request.user)

        if not can_edit:
            self.edit_not_available = True
            return False

        return has_permission

    def handle_no_permission(self):
        if self.edit_not_available:
            return redirect(
                reverse("edit_unavailable")
            )
        else:
            return redirect(
                reverse(
                    "forecast_cost_centre",
                    kwargs={
                        "cost_centre_code": self.cost_centre_code
                    }
                )
            )
