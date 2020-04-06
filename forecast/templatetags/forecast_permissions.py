from django import template

from forecast.utils.access_helpers import (
    can_view_forecasts,
    can_edit_at_least_one_cost_centre,
    can_edit_cost_centre,
)


register = template.Library()


@register.simple_tag
def is_forecast_user(user):
    return can_view_forecasts(user)


@register.simple_tag
def can_edit_cost_centre(user):
    return can_edit_at_least_one_cost_centre(user)


@register.simple_tag
def has_cost_centre_edit_permission(user, cost_centre_code):
    return can_edit_cost_centre(user, cost_centre_code)
