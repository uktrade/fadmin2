from django.db.models import F
from django.test import TestCase

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.models import (
    EndOfMonthStatus,
    forecast_budget_view_model,
)

from chartofaccountDIT.test.factories import (
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
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)


class MonthlyFigureSetup:
    def monthly_figure_update(self, period, amount, what='Forecast'):
        if what == 'Forecast':
            data_model = ForecastMonthlyFigure
        else:
            data_model = BudgetMonthlyFigure
        month_figure = data_model.objects.get(
            financial_period=FinancialPeriod.objects.get(financial_period_code=period),
            financial_code=self.financial_code_obj,
            financial_year=self.year_obj,
            archived_status=None,
        )
        month_figure.amount += amount
        month_figure.save()

    def monthly_figure_create(self, period, amount, what='Forecast'):
        if what == 'Forecast':
            data_model = ForecastMonthlyFigure
        else:
            data_model = BudgetMonthlyFigure
        month_figure = data_model.objects.create(
            financial_period=FinancialPeriod.objects.get(financial_period_code=period),
            financial_code=self.financial_code_obj,
            financial_year=self.year_obj,
            amount=amount,
        )
        month_figure.save()

    def __init__(self):
        group_name_test = "Test Group"
        group_code_test = "TestGG"
        directorate_name_test = "Test Directorate"
        directorate_code_test = "TestDD"
        cost_centre_code_test = 109076

        group = DepartmentalGroupFactory(
            group_code=group_code_test, group_name=group_name_test,
        )
        directorate = DirectorateFactory(
            directorate_code=directorate_code_test,
            directorate_name=directorate_name_test,
            group=group,
        )
        cost_centre = CostCentreFactory(
            directorate=directorate, cost_centre_code=cost_centre_code_test,
        )
        current_year = get_current_financial_year()
        programme_obj = ProgrammeCodeFactory()
        nac_obj = NaturalCodeFactory()
        project_obj = ProjectCodeFactory()
        self.year_obj = FinancialYear.objects.get(financial_year=current_year)

        self.financial_code_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cost_centre,
            natural_account_code=nac_obj,
            project_code=project_obj,
        )
        self.financial_code_obj.save

    def setup_forecast(self):
        for period in range(1, 16):
            self.monthly_figure_create(period, period * 100000)

    def setup_budget(self):
        for period in range(1, 16):
            self.monthly_figure_create(period, period * 100000, 'Budget')


class EndOfMonthForecastTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()

    # The following tests test_end_of_month_xxx checkes that only forecast is saved,
    # not actuals. This is tested by counting the records saved in the period tested.
    def test_end_of_month_apr(self):
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=1
        )
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 15)
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 30)

    def test_end_of_month_may(self):
        self.test_end_of_month_apr()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=2
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 44)

    def test_end_of_month_jun(self):
        self.test_end_of_month_may()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=3
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 57)

    def test_end_of_month_jul(self):
        self.test_end_of_month_jun()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=4
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 69)

    def test_end_of_month_aug(self):
        self.test_end_of_month_jul()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=5
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 80)

    def test_end_of_month_sep(self):
        self.test_end_of_month_aug()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=6
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 90)

    def test_end_of_month_oct(self):
        self.test_end_of_month_sep()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=7
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 99)

    def test_end_of_month_nov(self):
        self.test_end_of_month_oct()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=8
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 107)

    def test_end_of_month_dec(self):
        self.test_end_of_month_nov()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=9
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 114)

    def test_end_of_month_jan(self):
        self.test_end_of_month_dec()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=10
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 120)

    def test_end_of_month_feb(self):
        self.test_end_of_month_jan()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=11
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 125)

    def test_end_of_month_mar(self):
        self.test_end_of_month_feb()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=12
        )
        end_of_month_archive(end_of_month_info)
        count = ForecastMonthlyFigure.objects.all().count()
        self.assertEqual(count, 129)


class ReadArchivedForecastTest(TestCase, RequestFactoryBase):
    archived_figure = []

    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()
        for period in range(0, 16):
            self.archived_figure.append(0)

    def get_period_total(self, period):
        data_model = forecast_budget_view_model[period]
        tot_q = data_model.objects.annotate(
            total=F("apr")
            + F("may")
            + F("jun")
            + F("jul")
            + F("aug")
            + F("sep")
            + F("oct")
            + F("nov")
            + F("dec")
            + F("jan")
            + F("feb")
            + F("mar")
            + F("adj1")
            + F("adj2")
            + F("adj3")
        )
        return tot_q[0].total

    def get_current_total(self):
        return self.get_period_total(0)

    def set_archive_period(self, tested_period):
        total_before = self.get_current_total()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=tested_period
        )
        end_of_month_archive(end_of_month_info)
        # run a query giving the full total
        archived_total = self.get_period_total(tested_period)
        self.assertEqual(total_before, archived_total)
        change_amount = tested_period * 10000
        self.init_data.monthly_figure_update(tested_period + 1, change_amount)
        current_total = self.get_current_total()
        self.archived_figure[tested_period] = archived_total
        self.assertNotEqual(current_total, archived_total)
        self.assertEqual(current_total, (archived_total + change_amount))
        for period in range(1, tested_period + 1):
            self.assertEqual(
                self.archived_figure[period], self.get_period_total(period)
            )

    # The following tests check that the archived figures are not changed by
    # changing the current figures.
    def test_read_archived_figure_apr(self):
        tested_period = 1
        self.set_archive_period(tested_period)

    def test_read_archived_figure_may(self):
        tested_period = 2
        self.test_read_archived_figure_apr()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_jun(self):
        tested_period = 3
        self.test_read_archived_figure_may()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_jul(self):
        tested_period = 4
        self.test_read_archived_figure_jun()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_aug(self):
        tested_period = 5
        self.test_read_archived_figure_jul()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_sep(self):
        tested_period = 6
        self.test_read_archived_figure_aug()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_oct(self):
        tested_period = 7
        self.test_read_archived_figure_sep()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_nov(self):
        tested_period = 8
        self.test_read_archived_figure_oct()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_dec(self):
        tested_period = 9
        self.test_read_archived_figure_nov()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_jan(self):
        tested_period = 10
        self.test_read_archived_figure_dec()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_feb(self):
        tested_period = 11
        self.test_read_archived_figure_jan()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_mar(self):
        tested_period = 12
        self.test_read_archived_figure_feb()
        self.set_archive_period(tested_period)


class EndOfMonthBudgetTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_budget()

    # The following tests test_end_of_month_xxx checkes that only forecast is saved,
    # not actuals. This is tested by counting the records saved in the period tested.
    def test_end_of_month_apr(self):
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=1
        )
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 15)
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 30)

    def test_end_of_month_may(self):
        self.test_end_of_month_apr()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=2
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 44)

    def test_end_of_month_jun(self):
        self.test_end_of_month_may()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=3
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 57)

    def test_end_of_month_jul(self):
        self.test_end_of_month_jun()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=4
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 69)

    def test_end_of_month_aug(self):
        self.test_end_of_month_jul()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=5
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 80)

    def test_end_of_month_sep(self):
        self.test_end_of_month_aug()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=6
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 90)

    def test_end_of_month_oct(self):
        self.test_end_of_month_sep()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=7
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 99)

    def test_end_of_month_nov(self):
        self.test_end_of_month_oct()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=8
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 107)

    def test_end_of_month_dec(self):
        self.test_end_of_month_nov()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=9
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 114)

    def test_end_of_month_jan(self):
        self.test_end_of_month_dec()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=10
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 120)

    def test_end_of_month_feb(self):
        self.test_end_of_month_jan()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=11
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 125)

    def test_end_of_month_mar(self):
        self.test_end_of_month_feb()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=12
        )
        end_of_month_archive(end_of_month_info)
        count = BudgetMonthlyFigure.objects.all().count()
        self.assertEqual(count, 129)


class ReadArchivedBudgetTest(TestCase, RequestFactoryBase):
    archived_figure = []

    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_budget()
        for period in range(0, 16):
            self.archived_figure.append(0)

    def get_period_total(self, period):
        data_model = forecast_budget_view_model[period]
        tot_q = data_model.objects.all()
        return tot_q[0].budget

    def get_current_total(self):
        return self.get_period_total(0)

    def set_archive_period(self, tested_period):
        total_before = self.get_current_total()
        end_of_month_info = EndOfMonthStatus.objects.get(
            archived_period__financial_period_code=tested_period
        )
        end_of_month_archive(end_of_month_info)
        # run a query giving the full total
        archived_total = self.get_period_total(tested_period)
        self.assertEqual(total_before, archived_total)
        change_amount = tested_period * 10000
        self.init_data.monthly_figure_update(tested_period + 1, change_amount, 'budget')
        current_total = self.get_current_total()
        self.archived_figure[tested_period] = archived_total
        self.assertNotEqual(current_total, archived_total)
        self.assertEqual(current_total, (archived_total + change_amount))
        for period in range(1, tested_period + 1):
            self.assertEqual(
                self.archived_figure[period], self.get_period_total(period)
            )

    # The following tests check that the archived figures are not changed by
    # changing the current figures.
    def test_read_archived_figure_apr(self):
        tested_period = 1
        self.set_archive_period(tested_period)

    def test_read_archived_figure_may(self):
        tested_period = 2
        self.test_read_archived_figure_apr()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_jun(self):
        tested_period = 3
        self.test_read_archived_figure_may()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_jul(self):
        tested_period = 4
        self.test_read_archived_figure_jun()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_aug(self):
        tested_period = 5
        self.test_read_archived_figure_jul()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_sep(self):
        tested_period = 6
        self.test_read_archived_figure_aug()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_oct(self):
        tested_period = 7
        self.test_read_archived_figure_sep()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_nov(self):
        tested_period = 8
        self.test_read_archived_figure_oct()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_dec(self):
        tested_period = 9
        self.test_read_archived_figure_nov()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_jan(self):
        tested_period = 10
        self.test_read_archived_figure_dec()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_feb(self):
        tested_period = 11
        self.test_read_archived_figure_jan()
        self.set_archive_period(tested_period)

    def test_read_archived_figure_mar(self):
        tested_period = 12
        self.test_read_archived_figure_feb()
        self.set_archive_period(tested_period)
