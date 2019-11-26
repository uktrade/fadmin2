from forecast.models import MonthlyFigure


def get_forecast_monthly_figures_pivot(cost_centre_code):
    pivot_filter = {"cost_centre__cost_centre_code": "{}".format(
        cost_centre_code
    )}
    output = MonthlyFigure.pivot.pivot_data({}, pivot_filter)
    return list(output)
