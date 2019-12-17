import time

from behave import (
    given,
    when,
    then,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from features.environment import (
    create_test_user,
    copy_text,
    paste,
)

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    MonthlyFigure,
    MonthlyFigureAmount,
)

from forecast.test.factories import (
    ForecastPermissionFactory,
)


def check_error_message(context, msg):
    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "paste_error_msg"))
    )
    error_msg = context.browser.find_element_by_id(
        "paste_error_msg"
    ).get_attribute(
        'innerHTML'
    )

    assert error_msg == msg


@given(u'the user selects all rows in the edit forecast table')
def step_impl(context):
    create_test_user(context)

    # Add forecast view permission
    ForecastPermissionFactory(
        user=context.user,
    )

    context.browser.get(f'{context.base_url}/forecast/edit/{888812}/')

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "select_all"))
    )

    april_value = context.browser.find_element_by_id(
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    first_select = context.browser.find_element_by_id("select_all")
    first_select.click()


@given(u'the user selects a row in the edit forecast table')
def step_impl(context):
    create_test_user(context)

    # Add forecast view permission
    ForecastPermissionFactory(
        user=context.user,
    )

    context.browser.get(f'{context.base_url}/forecast/edit/{888812}/')

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "select_0"))
    )

    april_value = context.browser.find_element_by_id(
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    first_select = context.browser.find_element_by_id("select_0")
    first_select.click()


@when(u'the user pastes valid row data')
def step_impl(context):
    no_error_paste_text = "999999	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, no_error_paste_text)
    paste(context)


@when(u'the user pastes valid sheet data')
def step_impl(context):
    no_error_paste_text = "999999	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n111111	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"

    copy_text(context, no_error_paste_text)
    paste(context)


@when(u'the user pastes too many rows')
def step_impl(context):
    too_many_rows_paste_text = "999999	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n111111	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n222222	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, too_many_rows_paste_text)
    paste(context)


@then(u'the clipboard data is displayed in the forecast table')
def step_impl(context):
    time.sleep(2)

    april_value = context.browser.find_element_by_id(
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "1,000"


@when(u'the user pastes invalid row data')
def step_impl(context):
    error_paste_text = "This is a mistake..."
    copy_text(context, error_paste_text)
    paste(context)


@then(u'the incorrect format error is displayed')
def step_impl(context):
    check_error_message(
        context,
        "Your pasted data is not in the correct format",
    )


@then('the too few rows error is displayed')
def step_impl(context):
    check_error_message(
        context,
        "You have selected all forecast rows but the pasted data has too few rows.",
    )


@then('the too many rows error is displayed')
def step_impl(context):
    check_error_message(
        context,
        "You have selected all forecast rows but the pasted data has too many rows.",
    )


@when(u'the user pastes valid row data with actuals changed')
def step_impl(context):
    april = FinancialPeriod.objects.filter(
        period_long_name="April"
    ).first()
    april.actual_loaded = True
    april.save()

    no_error_paste_text = "999999	123456	1111111	2222222	3000	111.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, no_error_paste_text)
    paste(context)

    april.actual_loaded = False
    april.save()


@then(u'the actuals data is unchanged')
def step_impl(context):
    april_value = context.browser.find_element_by_id(
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )
    assert april_value == "0"


@when(u'the user pastes valid row data with a 5 decimal place value')
def step_impl(context):
    no_error_paste_text = "999999	123456	1111111	2222222	3000	1000.499999999	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, no_error_paste_text)
    paste(context)


@then(u'the stored value has been rounded correctly')
def step_impl(context):
    financial_code = FinancialCode.objects.filter(
        cost_centre_id=999999,
    ).first()

    monthly_figure = MonthlyFigure.objects.filter(
        financial_period_id=1,
        financial_code=financial_code,
    ).first()

    monthly_figure_amount = MonthlyFigureAmount.objects.filter(
        monthly_figure=monthly_figure,
    ).first()

    assert monthly_figure_amount.amount == 100000
