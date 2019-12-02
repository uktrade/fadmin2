import datetime
from behave import (
    given,
    when,
    then,
)

from django.test import TestCase, modify_settings

from django.conf import settings
from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY,
    get_user_model
)
from django.contrib.sessions.backends.db import SessionStore

from django.contrib.auth import get_user_model

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from core.test.factories import FinancialYearFactory
from core.myutils import get_current_financial_year

from forecast.test.factories import (
    ForecastPermissionFactory,
)

from costcentre.test.factories import (
    CostCentreFactory,
)

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    BudgetType,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from forecast.models import (
    MonthlyFigure,
)

from forecast.test.factories import FinancialPeriodFactory


def set_up_test_objects():
    cost_centre_code = 888812
    nac_code = 999999
    analysis_1_code = "1111111"
    analysis_2_code = "2222222"
    project_code_value = "3000"

    FinancialYearFactory()

    if BudgetType.objects.count() == 0:
        BudgetType.objects.create(
            budget_type_key="DEL",
            budget_type="Programme DEL",
        )
        BudgetType.objects.create(
            budget_type_key="AME",
            budget_type="Programme AME",
        )
        BudgetType.objects.create(
            budget_type_key="ADMIN",
            budget_type="Admin",
        )

    CostCentreFactory.create(
        cost_centre_code=cost_centre_code
    )

    programme = ProgrammeCodeFactory.create()
    nac_code = NaturalCodeFactory.create(natural_account_code=nac_code)
    project_code = ProjectCodeFactory.create(project_code=project_code_value)
    analysis_1 = Analysis1Factory.create(analysis1_code=analysis_1_code)
    analysis_2 = Analysis2Factory.create(analysis2_code=analysis_2_code)

    for financial_period in range(1, 13):
        financial_month = financial_period + 3

        if financial_month > 12:
            financial_month = financial_month - 12

        month_name = (
            financial_period,
            datetime.date(
                get_current_financial_year(),
                financial_month, 1
            ).strftime('%B')
        )[1]

        FinancialPeriodFactory(
            financial_period_code=financial_period,
            period_long_name=month_name,
            period_short_name=month_name[0:3],
            period_calendar_code=financial_month
        )

        monthly_figure = MonthlyFigure(
            financial_year_id=get_current_financial_year(),
            financial_period_id=financial_period,
            cost_centre_id=cost_centre_code,
            programme=programme,
            natural_account_code=nac_code,
            analysis1_code=analysis_1,
            analysis2_code=analysis_2,
            project_code=project_code,
            amount=0,
        )
        monthly_figure.save()


def create_test_user(context):
    if not hasattr(context, 'user'):
        test_user_email = "test@test.com"
        test_password = "test_password"

        test_user, _ = get_user_model().objects.get_or_create(
            email=test_user_email
        )
        test_user.is_staff = True
        test_user.is_superuser = True
        test_user.set_password(test_password)
        test_user.save()

        context.user = test_user

        client = context.test.client
        client.login(
            email=test_user_email,
            password=test_password,
        )

        # Then create the authenticated session using the new user credentials
        session = SessionStore()
        session[SESSION_KEY] = test_user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = test_user.get_session_auth_hash()
        session.save()

        # Finally, create the cookie dictionary
        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'secure': False,
            'path': '/',
        }

        context.browser.get(f'{context.base_url}/admin/login/')
        context.browser.add_cookie(cookie)
        context.browser.refresh()  # need to update page for logged in user
        context.browser.get(f'{context.base_url}/')


def paste(context):
    first_select = context.browser.find_element_by_id("clipboard-test")
    first_select.send_keys(Keys.CONTROL, "v")


def copy_text(context, text):
    context.browser.execute_script(
        """function copyToClipboard() {{
        const input = document.createElement('input');
        document.body.appendChild(input);
        input.value = "{}";
        input.id = "clipboard-test"
        input.focus();
        input.select();
        const isSuccessful = document.execCommand('copy');
        input.blur();
        }}
        copyToClipboard()
        """.format(text)
    )


@given(u'the user selects a row in the edit forecast table')
def step_impl(context):
    set_up_test_objects()

    create_test_user(context)

    # Add forecast view permission
    ForecastPermissionFactory(
        user=context.user,
    )

    context.browser.get(f'{context.base_url}/forecast/edit/{888812}/')

    WebDriverWait(context.browser, 5000).until(
        EC.presence_of_element_located((By.ID, "select_0"))
    )

    april_value = context.browser.find_element_by_id(
        "id_Apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    first_select = context.browser.find_element_by_id("select_0")
    first_select.click()


    # no_error_paste_text = "999999	Test	1111111	2222222	3000	1000	0	0	0	0	0	0	0	0	0	0	0"
    #
    # copy_text(context, no_error_paste_text)
    #
    # paste(context)

    # april_value = context.browser.find_element_by_id(
    #     "id_Apr_0"
    # ).get_attribute(
    #     'innerHTML'
    # )
    #
    # assert april_value == "1000"

    # error_paste_text = "Test..."
    #
    # WebDriverWait(context.browser, 5000).until(
    #     EC.presence_of_element_located((By.ID, "test..."))
    # )


@when(u'the user pastes valid data')
def step_impl(context):
    no_error_paste_text = "999999	Test	1111111	2222222	3000	1000	0	0	0	0	0	0	0	0	0	0	0"
    copy_text(context, no_error_paste_text)
    paste(context)


@then(u'the clipboard data is displayed in the forecast table')
def step_impl(context):
    april_value = context.browser.find_element_by_id(
        "id_Apr_0"
    ).get_attribute(
        'innerHTML'
    )
    assert april_value == "1000"

#
#
# @when(u'the user pastes')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: When the user pastes')
#
#
# @then(u'the clipboard data is displayed in the forecast table')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then the clipboard data is displayed in the forecast table')
