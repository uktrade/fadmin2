from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase
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
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.permission_shortcuts import assign_perm
from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
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


def create_budget(financial_code_obj, year_obj):
    budget_apr = 1000000
    budget_may = -1234567
    budget_july = 1234567
    budget_total = budget_apr + budget_may + budget_july
    # Save several months, and check that the total is displayed
    apr_budget = BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=1
        ),
        financial_code=financial_code_obj,
        financial_year=year_obj,
        amount=budget_apr
    )
    apr_budget.save
    may_budget = BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=2,
        ),
        amount=budget_may,
        financial_code=financial_code_obj,
        financial_year=year_obj
    )
    may_budget.save
    july_budget = BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=4,
        ),
        amount=budget_july,
        financial_code=financial_code_obj,
        financial_year=year_obj
    )
    july_budget.save
    return budget_total
