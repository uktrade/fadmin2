from behave import (
    given,
    when,
    then,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException

from features.environment import (
    TEST_COST_CENTRE_CODE,
    create_test_user,
)
from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastEditState,
    ForecastMonthlyFigure,
)
from forecast.test.factories import (
    FinancialPeriodFactory,
    ForecastEditStateFactory,
)
from core.models import FinancialYear
from core.myutils import get_current_financial_year
from core.test.factories import FinancialYearFactory


@given(u'the user views the edit forecast page with six months of actuals')
def step_impl(context):
    create_test_user(context)

    financial_year = FinancialYear.objects.first()
    financial_year = 6

    context.browser.get(
        f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/'
    )


@when(u'the user checks the actuals columns')
def step_impl(context):
    WebDriverWait(context.browser, 500).until(
        ec.presence_of_element_located((By.ID, "actuals-header"))
    )


@then(u'there are six actuals columns')
def step_impl(context):
    actuals_colspan = context.browser.find_element_by_id(
        "actuals-header"
    ).get_attribute(
        'colspan'
    )

    assert actuals_colspan == 6


# @given(u'the user views the edit forecast page with three months of actuals')
# def step_impl(context):
#     create_test_user(context)
#
#     financial_year = FinancialYear.objects.first()
#
#     context.browser.get(
#         f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/'
#     )
#
#
# @then(u'there are three actuals columns')
# def step_impl(context):
#     actuals_colspan = context.browser.find_element_by_id(
#         "actuals-header"
#     ).get_attribute(
#         'colspan'
#     )
#
#     assert actuals_colspan == 3