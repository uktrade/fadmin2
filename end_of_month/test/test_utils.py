from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.models import forecast_budget_view_model

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.myutils import get_current_financial_year

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
    def monthly_figure_update(self, period, amount, what="Forecast"):
        if what == "Forecast":
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

    def monthly_figure_create(self, period, amount, what="Forecast"):
        if what == "Forecast":
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
        group_name = "Test Group"
        self.group_code = "TestGG"
        directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        group_obj = DepartmentalGroupFactory(
            group_code=self.group_code, group_name=group_name,
        )
        directorate_obj = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=directorate_name,
            group=group_obj,
        )
        cost_centre_obj = CostCentreFactory(
            directorate=directorate_obj, cost_centre_code=self.cost_centre_code,
        )
        current_year = get_current_financial_year()
        programme_obj = ProgrammeCodeFactory()
        self.programme_code = programme_obj.programme_code
        nac_obj = NaturalCodeFactory()
        self.nac = nac_obj.natural_account_code
        project_obj = ProjectCodeFactory()
        self.project_code = project_obj.project_code
        self.year_obj = FinancialYear.objects.get(financial_year=current_year)

        self.financial_code_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cost_centre_obj,
            natural_account_code=nac_obj,
            project_code=project_obj,
        )
        self.financial_code_obj.save

    def setup_forecast(self):
        for period in range(1, 16):
            self.monthly_figure_create(period, period * 100000)

    def setup_budget(self):
        for period in range(1, 16):
            self.monthly_figure_create(period, period * 100000, "Budget")


class SetFullYearArchive(MonthlyFigureSetup):
    archived_forecast = []
    archived_budget = []

    def set_period_total(self, period):
        data_model = forecast_budget_view_model[period]
        tot_q = data_model.objects.all()
        self.archived_forecast[period] = (
            tot_q[0].apr
            + tot_q[0].may
            + tot_q[0].jun
            + tot_q[0].jul
            + tot_q[0].aug
            + tot_q[0].sep
            + tot_q[0].oct
            + tot_q[0].nov
            + tot_q[0].dec
            + tot_q[0].jan
            + tot_q[0].feb
            + tot_q[0].mar
            + tot_q[0].adj1
            + tot_q[0].adj2
            + tot_q[0].adj3
        )
        self.archived_budget[period] = tot_q[0].budget

    def set_archive_period(self, last_archived_period=13):
        if last_archived_period > 13:
            last_archived_period = 13
        for tested_period in range(1, last_archived_period):
            end_of_month_archive(tested_period)
            # save the full total
            self.set_period_total(tested_period)
            change_amount = tested_period * 10000
            self.monthly_figure_update(tested_period + 1, change_amount, "Forecast")
            change_amount = tested_period * 1000
            self.monthly_figure_update(tested_period + 1, change_amount, "Budget")
        self.set_period_total(0)

    def __init__(self, last_archived_period=16):
        super().__init__()
        self.setup_forecast()
        self.setup_budget()
        # prepares the lists used to store the totals
        for period in range(0, last_archived_period):
            self.archived_forecast.append(0)
            self.archived_budget.append(0)
        self.set_archive_period(last_archived_period)
