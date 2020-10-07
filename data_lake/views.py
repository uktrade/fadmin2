import csv

from django.utils.decorators import decorator_from_middleware

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .hawk import (
    HawkAuthentication,
    HawkResponseMiddleware,
)

from core.utils.generic_helpers import get_current_financial_year

from end_of_month.models import forecast_budget_view_model

from forecast.views.base import (
    DITForecastMixin,
    ForecastViewTableMixin,
)
from forecast.utils.query_fields import ForecastQueryFields
from forecast.models import FinancialPeriod

from django.http import HttpResponse


import logging


logger = logging.getLogger(__name__)


class ForecastViewSet(
    ViewSet,
):
    authentication_classes = (HawkAuthentication,)
    permission_classes = ()

    @decorator_from_middleware(HawkResponseMiddleware)
    def list(self, request):
        return Response("Hello!")


def forecast_query_iterator(queryset, keys_dict, period_list, forecast_period, year):
    for obj in queryset:
        row = []
        for field in keys_dict.keys():
            val = obj[field]
            if val is None:
                val = ""
            row.append(val)
        row.append(obj["Budget"])

        for period in period_list:
            row.append(obj[period])

        row.append(forecast_period)
        row.append(year)

        yield row


def haha(request):
    # get relevant financial periods
    actual_periods_qs = FinancialPeriod.objects.filter(
        actual_loaded=True
    ).values_list("financial_period_code", flat=True)

    actual_periods = [0, ] + list(actual_periods_qs)

    logger.error(actual_periods)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=forecast.csv"
    writer = csv.writer(response, csv.excel)
    response.write(u"\ufeff".encode("utf8"))  # Excel needs UTF-8 to open the file

    # Titles
    writer.writerow([
        "Group name",
        "Group code",
        "Directorate name",
        "Directorate code",
        "Cost Centre name",
        "Cost Centre code",
        "Budget grouping",
        "Expenditure type"
        "Expenditure type description",
        "Budget Type",
        "Budget category",
        "Budget category",
        "Budget/Forecast NAC",
        "Budget/Forecast NAC description",
        "PO/Actual NAC",
        "Natural Account code description",
        "NAC Expenditure type",
        "Programme code",
        "Programme code description",
        "Contract code",
        "Contract description",
        "Market code",
        "Market description",
        "Project code",
        "Project description",
        "Budget",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
        "Jan",
        "Feb",
        "Mar",
        "Adj1",
        "Adj2",
        "Adj3",
        "Period",
        "Year",
        # "Forecast outturn",
        # "Variance -overspend/underspend",
        # "Year to Date Actuals"
    ])

    period_list = FinancialPeriod.financial_period_info.period_display_list()
    current_year = get_current_financial_year()

    for forecast_period in actual_periods:
        fields = ForecastQueryFields(forecast_period)

        data_model = forecast_budget_view_model[forecast_period]
        period_query = data_model.view_data.raw_data_annotated(
            fields.VIEW_FORECAST_DOWNLOAD_COLUMNS,
        )

        for data_row in forecast_query_iterator(
            period_query,
            fields.VIEW_FORECAST_DOWNLOAD_COLUMNS,
            period_list,
            forecast_period,
            current_year,
        ):
            writer.writerow(data_row)

    return response
