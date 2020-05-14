from behave import (
    given,
    when,
    then,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from features.environment import (
    TEST_COST_CENTRE_CODE,
    create_test_user,
)

from chartofaccountDIT.models import ProgrammeCode

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)


@given(u'the user views the edit forecast page with six months of actuals')
def step_impl(context):
    # ForecastMonthlyFigure.objects.all().delete()
    # FinancialCode.objects.all().delete()
    # programme_list = ProgrammeCode.objects.all()
    # monthly_amount = 0
    # # actual = FinancialPeriod.objects.all()
    # # actual.actual_loaded = False
    # for programme_fk in programme_list:
    #     monthly_amount += 10

    for i in range(1, 6):
        actual = FinancialPeriod.objects.get(financial_period_code=i)
        actual.actual_loaded = True
        actual.save()

    create_test_user(context)

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


@given(u'the user views the edit forecast page with three months of actuals')
def step_impl(context):
    create_test_user(context)

    for i in range(1, 4):
        actual = FinancialPeriod.objects.get(financial_period_code=i)
        actual.actual_loaded = True
        actual.save()

        context.browser.get(
            f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/'
        )


@then(u'there are three actuals columns')
def step_impl(context):
    actuals_colspan = context.browser.find_element_by_id(
        "actuals-header"
    ).get_attribute(
        'colspan'
    )

    assert actuals_colspan == 3
