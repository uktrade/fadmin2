from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from forecast.models import (
    ForecastMonthlyFigure,
)
from forecast.test.factories import (
    FinancialCodeFactory,
    ForecastMonthlyFigureFactory,
)


class ForecastManagementCommandTest(TestCase):
    def test_remove_forecast_data(self):
        financial_code = FinancialCodeFactory()

        # Create monthly figures
        ForecastMonthlyFigureFactory(
            financial_code=financial_code,
        )
        ForecastMonthlyFigureFactory(
            financial_code=financial_code,
        )

        assert ForecastMonthlyFigure.objects.count() == 2

        # Run remove management command
        out = StringIO()
        call_command('remove_forecast_data', stdout=out)

        assert "All forecast objects deleted" in out.getvalue()
        assert ForecastMonthlyFigure.objects.count() == 0
