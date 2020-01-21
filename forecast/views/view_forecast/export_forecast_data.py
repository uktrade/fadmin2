from core.exportutils import export_query_to_excel

from forecast.models import ForecastBudgetDataView
from forecast.utils.query_fields import (
    COST_CENTRE_CODE,
    DIRECTORATE_CODE,
    DOWNLOAD_COLUMNS,
    GROUP_CODE,
)


def export_forecast_data_dit(request):
    q = ForecastBudgetDataView.sub_total.raw_data(DOWNLOAD_COLUMNS)
    return export_query_to_excel(q, DOWNLOAD_COLUMNS, "DIT")

def export_forecast_data_group(request, group_code):
    filter = {GROUP_CODE: group_code}
    q = ForecastBudgetDataView.sub_total.raw_data(DOWNLOAD_COLUMNS, filter)
    return export_query_to_excel(q, DOWNLOAD_COLUMNS, group_code)

def export_forecast_data_directorate(request, directorate_code):
    filter = {DIRECTORATE_CODE: directorate_code}
    q = ForecastBudgetDataView.sub_total.raw_data(DOWNLOAD_COLUMNS, filter)
    return export_query_to_excel(q, DOWNLOAD_COLUMNS, directorate_code)

def export_forecast_data_cost_centre(request, cost_centre):
    filter = {COST_CENTRE_CODE: cost_centre}
    q = ForecastBudgetDataView.sub_total.raw_data(DOWNLOAD_COLUMNS, filter)
    return export_query_to_excel(q, DOWNLOAD_COLUMNS, cost_centre)
