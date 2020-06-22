from django.db.models import F
from django.test import TestCase

from end_of_month.end_of_month_actions import (
    ArchiveMonthAlreadyArchivedError,
    ArchiveMonthArchivedPastError,
    ArchiveMonthInvalidPeriodError,
    DeleteNonExistingArchiveError,
    delete_end_of_month_archive,
    delete_last_end_of_month_archive,
    end_of_month_archive,
)
from end_of_month.models import (
    MonthlyTotalBudget,
    forecast_budget_view_model,
)
from end_of_month.test.test_utils import (
    MonthlyFigureSetup,
)

from core.test.test_base import RequestFactoryBase

from forecast.models import (
    BudgetMonthlyFigure,
    ForecastMonthlyFigure,
)


class DeleteEndOfMonthArchiveTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()

    # def test_error_invalid_period(self):
    #     with self.assertRaises(DeleteNonExistingArchiveError):
    #         delete_last_end_of_month_archive()
    #     with self.assertRaises(ArchiveMonthInvalidPeriodError):
    #         delete_end_of_month_archive(0)
    #     with self.assertRaises(DeleteNonExistingArchiveError):
    #         delete_end_of_month_archive(1)
    #
    def test_delete_latest_period(self):
        initial_count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(initial_count, 15)
        end_of_month_archive(1)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 30)
        delete_last_end_of_month_archive()
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, initial_count)

    def test_delete_selected_period(self):
        end_of_month_archive(1)
        initial_count = ForecastMonthlyFigure.objects.all().count()
        end_of_month_archive(2)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertNotEqual(count, initial_count)
        delete_end_of_month_archive(2)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, initial_count)
