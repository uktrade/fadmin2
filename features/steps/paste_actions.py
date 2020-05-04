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
    copy_text,
    paste,
)

from forecast.models import (
    FinancialPeriod,
)


def check_error_message(context, msg, ):
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

    context.browser.get(f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/')

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_4"))
    )

    april_value = context.browser.find_element_by_id(
        "id_0_1"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    first_select = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "select_all"))
    )

    first_select.click()


@given(u'the user selects a row in the edit forecast table')
def step_impl(context):
    create_test_user(context)

    context.browser.get(
        f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/'
    )

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "select_row_0"))
    )

    april_value = context.browser.find_element_by_id(
        "id_0_1"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    first_select = context.browser.find_element_by_id("select_row_0")
    first_select.click()


@when(u'the user pastes valid row data')
def step_impl(context):
    paste_text = "123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes valid sheet data')
def step_impl(context):
    paste_text = "123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n123456	Test	999999	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"

    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes valid sheet data with column headers')
def step_impl(context):
    paste_text = "Programme code	Programme code Description	Natural Account code	Natural Account Code Description	Contract Code	Market Code	Project Code	Budget	Apr	May	Jun	Jul	Aug	Sep	Oct	Nov	Dec	Jan	Feb	Mar	Forecast outturn	Variance -overspend/underspend	Year to Date Actuals	Group name	Group code	Directorate name	Directorate code	Cost Centre name	Cost Centre code	Budget Grouping	Expenditure type	Expenditure type description	Budget type	Budget Category	Budget/Forecast NAC	Budget/Forecast NAC Description	NAC Expenditure Type	Contract Description	Market Description	Project Description"
    paste_text += "\\n123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n123456	Test	999999	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"

    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes sheet data with invalid column headers')
def step_impl(context):
    paste_text = "Natural Account code	Programme code Description	Programme code	Natural Account Code Description	Contract Code	Market Code	Project Code	Budget	Apr	May	Jun	Jul	Aug	Sep	Oct	Nov	Dec	Jan	Feb	Mar	Forecast outturn	Variance -overspend/underspend	Year to Date Actuals	Group name	Group code	Directorate name	Directorate code	Cost Centre name	Cost Centre code	Budget Grouping	Expenditure type	Expenditure type description	Budget type	Budget Category	Budget/Forecast NAC	Budget/Forecast NAC Description	NAC Expenditure Type	Contract Description	Market Description	Project Description"
    paste_text += "\\n123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n123456	Test	999999	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"

    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes too many rows')
def step_impl(context):
    too_many_rows_paste_text = "123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n123456	Test	999999	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n123456	Test	n333333	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, too_many_rows_paste_text)
    paste(context)


@then(u'the clipboard data is displayed in the forecast table')
def step_impl(context):
    april_value = context.browser.find_element_by_id(
        "id_0_1"
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

    paste_text = "123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n999999	Test	123456	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)

    april.actual_loaded = False
    april.save()


@then(u'the actuals data is unchanged')
def step_impl(context):
    april_value = context.browser.find_element_by_id(
        "id_0_1"
    ).get_attribute(
        'innerHTML'
    )
    assert april_value == "0"


@when(u'the user pastes valid row data with a 5 decimal place value')
def step_impl(context):
    paste_text = "123456	Test	111111	Test	1111111	2222222	3000	0	1000.49999	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes too many column row data')
def step_impl(context):
    paste_text = "123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n123456	Test	999999	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@then(u'the too many columns error message is displayed')
def step_impl(context):
    check_error_message(
        context,
        'Your pasted data does not '
        'match the expected format. '
        'There are too many columns.'
    )


@when(u'the user pastes too few column row data')
def step_impl(context):
    paste_text = "123456	Test	111111	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@then(u'the too few columns error message is displayed')
def step_impl(context):
    check_error_message(
        context,
        'Your pasted data does not '
        'match the expected format. '
        'There are not enough columns.'
    )


@when(u'the user pastes mismatched columns')
def step_impl(context):
    paste_text = "111111	Test	333444	Test	1111111	2222222	3000	0	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@then(u'the mismatched columns error message is displayed')
def step_impl(context):
    check_error_message(
        context,
        'There is a mismatch between your pasted and selected rows. Please check the following columns: "Programme", "Natural account code".'
    )
