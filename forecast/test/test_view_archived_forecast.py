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

from end_of_month.test.test_utils import (
    MonthlyFigureSetup,
    SetFullYearArchive,
)

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
from forecast.test.test_utils import (
    create_budget,
    format_forecast_figure,
)
from forecast.views.view_forecast.forecast_summary import (
    CostCentreView,
    DITView,
    DirectorateView,
    GroupView,
)

TOTAL_COLUMN = -5
SPEND_TO_DATE_COLUMN = -2
UNDERSPEND_COLUMN = -4

HIERARCHY_TABLE_INDEX = 0
PROGRAMME_TABLE_INDEX = 1
EXPENDITURE_TABLE_INDEX = 2
PROJECT_TABLE_INDEX = 3

class ViewArchivedForecastHierarchyTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        self.archive = SetFullYearArchive()

    # def check_programme_table(self, table, prog_index=1):
    #     programme_rows = table.find_all("tr")
    #     first_prog_cols = programme_rows[2].find_all("td")
    #     assert first_prog_cols[prog_index + 1].get_text().strip() == \
    #         self.archive.programme_code_test
    #
    #     last_programme_cols = programme_rows[-1].find_all("td")
    #     # Check the total for the year
    #     assert last_programme_cols[TOTAL_COLUMN].get_text().strip() == \
    #         format_forecast_figure(self.year_total / 100)
    #     # Check the difference between budget and year total
    #     assert last_programme_cols[UNDERSPEND_COLUMN].get_text().strip() == \
    #         format_forecast_figure(self.underspend_total / 100)
    #     # Check the spend to date
    #     assert last_programme_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
    #         format_forecast_figure(self.spend_to_date_total / 100)
    #
    # def check_expenditure_table(self, table):
    #     expenditure_rows = table.find_all("tr")
    #     first_expenditure_cols = expenditure_rows[2].find_all("td")
    #     assert (first_expenditure_cols[1].get_text().strip() == '—')
    #     assert first_expenditure_cols[2].get_text().strip() == format_forecast_figure(
    #         self.budget / 100
    #     )
    #
    #     last_expenditure_cols = expenditure_rows[-1].find_all("td")
    #     # Check the total for the year
    #     assert last_expenditure_cols[TOTAL_COLUMN].get_text().strip() == \
    #         format_forecast_figure(self.year_total / 100)
    #     # Check the difference between budget and year total
    #     assert last_expenditure_cols[UNDERSPEND_COLUMN].get_text().strip() == \
    #         format_forecast_figure(self.underspend_total / 100)
    #     # Check the spend to date
    #     assert last_expenditure_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
    #         format_forecast_figure(self.spend_to_date_total / 100)
    #
    # def check_project_table(self, table):
    #     project_rows = table.find_all("tr")
    #     first_project_cols = project_rows[2].find_all("td")
    #
    #     assert first_project_cols[1].get_text().strip() == self.project_obj.project_code
    #     assert first_project_cols[3].get_text().strip() == format_forecast_figure(
    #         self.budget / 100
    #     )
    #
    #     last_project_cols = project_rows[-1].find_all("td")
    #     # Check the total for the year
    #     assert last_project_cols[TOTAL_COLUMN].get_text().strip() == \
    #         format_forecast_figure(self.year_total / 100)
    #
    def myassertEqual(self, p1, p2):
        print(f'{p1} compared to {p2}')

    def check_hierarchy_table(self, table, hierarchy_element, offset, period):
        hierarchy_rows = table.find_all("tr")
        first_hierarchy_cols = hierarchy_rows[2].find_all("td")
        self.assertEqual( first_hierarchy_cols[2 + offset].get_text().strip(),
            str(hierarchy_element))

        budget_col = 3 + offset
        self.assertEqual (first_hierarchy_cols[budget_col].get_text().strip(),
            format_forecast_figure(self.archive.archived_budget[period] / 100))

        last_hierarchy_cols = hierarchy_rows[-1].find_all("td")
        # Check the total for the year
        self.assertEqual(last_hierarchy_cols[TOTAL_COLUMN].get_text().strip(),
            format_forecast_figure(self.archive.archived_forecast[period] / 100))

    def test_view_cost_centre_summary(self):
        test_period = 1
        resp = self.factory_get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.archive.cost_centre_code,
                    "period": test_period,
                },
            ),
            CostCentreView,
            cost_centre_code=self.archive.cost_centre_code,
            period=test_period,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")
        print(soup.prettify())
        # self.assertContains(resp.content, f'<option value="{test_period}" selected>')

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18


        # Check that the first table displays the cost centre code
        # self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
        #                            self.archive.cost_centre_code, 0, test_period)
        #

    #     # Check that the second table displays the programme and the correct totals
    #     # The programme table in the cost centre does not show the 'View'
    #     # so the programme is displayed in a different column
    #     self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)
    #
    #     # Check that the third table displays the expenditure and the correct totals
    #     self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])
    #
    #     # Check that the second table displays the project and the correct totals
    #     self.check_project_table(tables[PROJECT_TABLE_INDEX])
    #
    # def test_view_directorate_summary(self):
    #     resp = self.factory_get(
    #         reverse(
    #             "forecast_directorate",
    #             kwargs={
    #                 'directorate_code': self.directorate.directorate_code,
    #                 'period': 0,
    #             },
    #         ),
    #         DirectorateView,
    #         directorate_code=self.directorate.directorate_code,
    #         period=0,
    #     )
    #
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertContains(resp, "govuk-table")
    #     soup = BeautifulSoup(resp.content, features="html.parser")
    #
    #     # Check that there are 4 tables on the page
    #     tables = soup.find_all("table", class_="govuk-table")
    #     assert len(tables) == 4
    #
    #     # Check that the first table displays the cost centre code
    #
    #     # Check that all the subtotal hierachy_rows exist
    #     table_rows = soup.find_all("tr", class_="govuk-table__row")
    #     assert len(table_rows) == 18
    #
    #     self.check_negative_value_formatted(soup)
    #
    #     self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
    #                                self.cost_centre.cost_centre_name, 0)
    #
    #     # Check that the second table displays the programme and the correct totals
    #     self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])
    #
    #     # Check that the third table displays the expenditure and the correct totals
    #     self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])
    #
    #     # Check that the second table displays the project and the correct totals
    #     self.check_project_table(tables[PROJECT_TABLE_INDEX])
    #
    # def test_view_group_summary(self):
    #     response = self.factory_get(
    #         reverse(
    #             "forecast_group",
    #             kwargs={
    #                 'group_code': self.group.group_code,
    #                 'period': 0,
    #             },
    #         ),
    #         GroupView,
    #         group_code=self.group.group_code,
    #         period=0,
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "govuk-table")
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #
    #     # Check that there are 4 tables on the page
    #     tables = soup.find_all("table", class_="govuk-table")
    #     assert len(tables) == 4
    #
    #     # Check that the first table displays the cost centre code
    #
    #     # Check that all the subtotal hierachy_rows exist
    #     table_rows = soup.find_all("tr", class_="govuk-table__row")
    #     assert len(table_rows) == 18
    #
    #     self.check_negative_value_formatted(soup)
    #
    #     self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
    #                                self.directorate.directorate_name, 0)
    #     # Check that the second table displays the programme and the correct totals
    #     self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])
    #
    #     # Check that the third table displays the expenditure and the correct totals
    #     self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])
    #
    #     # Check that the second table displays the project and the correct totals
    #     self.check_project_table(tables[PROJECT_TABLE_INDEX])
    #
    # def test_view_dit_summary(self):
    #     response = self.factory_get(
    #         reverse(
    #             "forecast_dit",
    #             kwargs={
    #                 'period': 0,
    #             },
    #         ),
    #         DITView,
    #         period=0,
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "govuk-table")
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #
    #     # Check that there are 4 tables on the page
    #     tables = soup.find_all("table", class_="govuk-table")
    #     assert len(tables) == 4
    #
    #     # Check that the first table displays the cost centre code
    #
    #     # Check that all the subtotal hierarchy_rows exist
    #     table_rows = soup.find_all("tr", class_="govuk-table__row")
    #     assert len(table_rows) == 18
    #
    #     self.check_negative_value_formatted(soup)
    #
    #     self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
    #                                self.group_name, 0)
    #     # Check that the second table displays the programme and the correct totals
    #     self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])
    #
    #     # Check that the third table displays the expenditure and the correct totals
    #     self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])
    #
    #     # Check that the second table displays the project and the correct totals
    #     self.check_project_table(tables[PROJECT_TABLE_INDEX])

