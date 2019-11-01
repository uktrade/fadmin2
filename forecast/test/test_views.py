from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import intcomma
from django.test import RequestFactory, TestCase
from django.urls import reverse

from guardian.shortcuts import assign_perm

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from costcentre.test.factories import CostCentreFactory

from forecast.models import FinancialPeriod
from forecast.test.factories import MonthlyFigureFactory
from forecast.views import EditForecastView


class ViewPermissionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.cost_centre_code = 109076
        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )

        self.test_user.set_password(self.test_password)

    def test_edit_forecast_view(self):
        self.assertFalse(self.test_user.has_perm("change_costcentre", self.cost_centre))

        request = self.factory.get(reverse("edit_forecast"))
        request.user = self.test_user

        resp = EditForecastView.as_view()(request)

        # Should have been redirected (no permission)
        self.assertEqual(resp.status_code, 302)

        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        self.assertTrue(self.test_user.has_perm("change_costcentre", self.cost_centre))
        self.assertTrue(self.test_user.has_perm("view_costcentre", self.cost_centre))

        request = self.factory.get(reverse("edit_forecast"))
        request.user = self.test_user

        resp = EditForecastView.as_view()(request)

        # Should be allowed
        self.assertEqual(resp.status_code, 200)


class AddForecastRowTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.programme = ProgrammeCodeFactory.create()
        self.nac = NaturalCodeFactory.create(natural_account_code=999999)

        self.cost_centre_code = 109076
        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )

        self.test_user.set_password(self.test_password)

    def test_view_add_row(self):
        # Set up test objects
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        request = self.factory.get(reverse("edit_forecast"))
        request.user = self.test_user
        edit_resp = EditForecastView.as_view()(request)

        self.assertEqual(edit_resp.status_code, 200)

        self.assertContains(edit_resp, "govuk-table")
        soup = BeautifulSoup(edit_resp.content, features="html.parser")
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # There should only be 2 rows (for the header and footer)
        assert len(table_rows) == 2

        add_resp = self.client.get(reverse("add_forecast_row"))
        self.assertEqual(add_resp.status_code, 200)

        # add_forecast_row
        add_row_resp = self.client.post(
            reverse("add_forecast_row"),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
            },
            follow=True,
        )

        self.assertEqual(add_row_resp.status_code, 200)

        self.assertContains(add_row_resp, "govuk-table")
        soup = BeautifulSoup(add_row_resp.content, features="html.parser")
        table_rows = soup.find_all("tr", class_="govuk-table__row")

        # Now we should have 3 rows (header, footer and new row)
        assert len(table_rows) == 3


class ViewCostCentreDashboard(TestCase):
    cost_centre_code = 109076
    amount = 9876543

    def setUp(self):
        self.apr_amount = MonthlyFigureFactory.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            cost_centre=CostCentreFactory.create(
                cost_centre_code=self.cost_centre_code
            ),
            amount=self.amount,
        )

    def test_view_cost_centre_dashboard(self):
        resp = self.client.get(reverse("pivotmulti"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")

        soup = BeautifulSoup(resp.content, features="html.parser")
        # Check that there are 3 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 3

        # Check that the first table displays the cost centre code
        rows = tables[0].find_all("tr")
        cols = rows[1].find_all("td")
        assert int(cols[2].get_text()) == self.cost_centre_code
        # Check the April value
        assert cols[4].get_text() == intcomma(self.amount)
        # Check the total for the year
        assert cols[-3].get_text() == intcomma(self.amount)
        # Check the difference between budget and year total
        assert cols[-2].get_text() == intcomma(-self.amount)
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 14
