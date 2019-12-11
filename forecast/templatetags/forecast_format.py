import calendar

from django import template

register = template.Library()


@register.filter()
def format_figure(value, column):
    if str(column) in calendar.month_name:
        figure_value = int(value) / 100
        return f'{figure_value:.2f}'

    return value
