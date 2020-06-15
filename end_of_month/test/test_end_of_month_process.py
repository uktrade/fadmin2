from datetime import datetime

from bs4 import BeautifulSoup


from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
    Permission,
)
from django.core.exceptions import PermissionDenied
from django.test import (
    TestCase,
)
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    ExpenditureCategoryFactory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.myutils import get_current_financial_year
from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastEditState,
    ForecastMonthlyFigure,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.factories import (
    FinancialCodeFactory,
)
from forecast.test.test_utils import create_budget
from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastFigureView,
    EditForecastView,
)
from forecast.views.view_forecast.expenditure_details import (
    CostCentreExpenditureDetailsView,
    DITExpenditureDetailsView,
    DirectorateExpenditureDetailsView,
    GroupExpenditureDetailsView,
)
from forecast.views.view_forecast.forecast_summary import (
    CostCentreView,
    DITView,
    DirectorateView,
    GroupView,
)
from forecast.views.view_forecast.programme_details import (
    DITProgrammeDetailsView,
    DirectorateProgrammeDetailsView,
    GroupProgrammeDetailsView,
)

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.models import EndOfMonthStatus


TOTAL_COLUMN = -5
SPEND_TO_DATE_COLUMN = -2
UNDERSPEND_COLUMN = -4

HIERARCHY_TABLE_INDEX = 0
PROGRAMME_TABLE_INDEX = 1
EXPENDITURE_TABLE_INDEX = 2
PROJECT_TABLE_INDEX = 3


def format_forecast_figure(value):
    return f'{round(value):,d}'

def monthly_figure_save(year_obj, financial_code_obj, period):
    month_figure = ForecastMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=period
        ),
        financial_code=financial_code_obj,
        financial_year=year_obj,
        amount=period*100000
    )
    month_figure.save


class Monthly_figure_setup():

    def monthly_figure_save(self, period):
        month_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=period
            ),
            financial_code=self.financial_code_obj,
            financial_year=self.year_obj,
            amount=period * 100000
        )
        month_figure.save

    def __init__(self):
        group_name_test = "Test Group"
        group_code_test = "TestGG"
        directorate_name_test = "Test Directorate"
        directorate_code_test = "TestDD"
        cost_centre_code_test = 109076

        group = DepartmentalGroupFactory(
            group_code=group_code_test,
            group_name=group_name_test,
        )
        directorate = DirectorateFactory(
            directorate_code=directorate_code_test,
            directorate_name=directorate_name_test,
            group=group,
        )
        cost_centre = CostCentreFactory(
            directorate=directorate,
            cost_centre_code=cost_centre_code_test,
        )
        current_year = get_current_financial_year()
        amount_apr = 100000
        programme_obj = ProgrammeCodeFactory()
        nac_obj = NaturalCodeFactory()
        project_obj = ProjectCodeFactory()
        self. year_obj = FinancialYear.objects.get(
            financial_year=current_year
        )

        self.financial_code_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cost_centre,
            natural_account_code=nac_obj,
            project_code=project_obj
        )
        self.financial_code_obj.save
        for month in range(1,13):
            self.monthly_figure_save(month)


class EndOfMonthTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()
        Monthly_figure_setup()

    def test_end_of_month_apr(self):
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=1
        )
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 12)
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 24)

    def test_end_of_month_may(self):
        self.test_end_of_month_apr()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=2
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 35)

    def test_end_of_month_jun(self):
        self.test_end_of_month_may()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=3
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 45)

    def test_end_of_month_jul(self):
        self.test_end_of_month_jun()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=4
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 54)

    def test_end_of_month_aug(self):
        self.test_end_of_month_jul()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=5
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 62)

    def test_end_of_month_sep(self):
        self.test_end_of_month_aug()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=6
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 69)

    def test_end_of_month_oct(self):
        self.test_end_of_month_sep()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=7
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 75)

    def test_end_of_month_nov(self):
        self.test_end_of_month_oct()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=8
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 80)

    def test_end_of_month_dec(self):
        self.test_end_of_month_nov()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=9
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 84)

    def test_end_of_month_jan(self):
        self.test_end_of_month_dec()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=10
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 87)

    def test_end_of_month_feb(self):
        self.test_end_of_month_jan()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=11
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 89)

    def test_end_of_month_mar(self):
        self.test_end_of_month_feb()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=12
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 90)
