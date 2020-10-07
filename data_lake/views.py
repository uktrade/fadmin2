from django.utils.decorators import decorator_from_middleware

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .hawk import (
    HawkAuthentication,
    HawkResponseMiddleware,
)

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
        pass


def haha(request):
    # get relevant financial periods
    actual_periods_qs = FinancialPeriod.objects.filter(
        actual_loaded=True
    ).values_list("financial_period_code", flat=True)

    actual_periods = [0, ] + list(actual_periods_qs)

    period_output = []

    logger.error(actual_periods)

    for period in actual_periods:
        fields = ForecastQueryFields(period)

        data_model = forecast_budget_view_model[period]
        period_query = data_model.view_data.raw_data_annotated(
            fields.VIEW_FORECAST_DOWNLOAD_COLUMNS,
        )
        period_output.append(
            period_query,
        )

    return HttpResponse(period_output)
