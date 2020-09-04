# from datetime import datetime
#
# from bs4 import BeautifulSoup
#
#
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import (
#     Group,
#     Permission,
# )
# from django.core.exceptions import PermissionDenied
# from django.test import (
#     TestCase,
# )
# from django.urls import reverse
#
# from chartofaccountDIT.test.factories import (
#     Analysis1Factory,
#     Analysis2Factory,
#     ExpenditureCategoryFactory,
#     NaturalCodeFactory,
#     ProgrammeCodeFactory,
#     ProjectCodeFactory,
# )
#
# from core.models import FinancialYear
# from core.test.test_base import RequestFactoryBase
# from core.utils.generic_helpers import get_current_financial_year
#
# from costcentre.test.factories import (
#     CostCentreFactory,
#     DepartmentalGroupFactory,
#     DirectorateFactory,
# )
#
# from forecast.models import (
#     FinancialCode,
#     FinancialPeriod,
#     ForecastEditState,
#     ForecastMonthlyFigure,
# )
# from forecast.permission_shortcuts import assign_perm
# from forecast.test.factories import (
#     FinancialCodeFactory,
# )
# from forecast.test.test_utils import (
#     create_budget,
#     format_forecast_figure,
# )
# from forecast.views.edit_forecast import (
#     AddRowView,
#     ChooseCostCentreView,
#     EditForecastFigureView,
#     EditForecastView,
# )
# from forecast.views.view_forecast.expenditure_details import (
#     CostCentreExpenditureDetailsView,
#     DITExpenditureDetailsView,
#     DirectorateExpenditureDetailsView,
#     GroupExpenditureDetailsView,
# )
# from forecast.views.view_forecast.forecast_summary import (
#     CostCentreView,
#     DITView,
#     DirectorateView,
#     GroupView,
# )
# from forecast.views.view_forecast.programme_details import (
#     DITProgrammeDetailsView,
#     DirectorateProgrammeDetailsView,
#     GroupProgrammeDetailsView,
# )
#
# TOTAL_COLUMN = -5
# SPEND_TO_DATE_COLUMN = -2
# UNDERSPEND_COLUMN = -4
#
# HIERARCHY_TABLE_INDEX = 0
# PROGRAMME_TABLE_INDEX = 1
# EXPENDITURE_TABLE_INDEX = 2
# PROJECT_TABLE_INDEX = 3
#
#
#
# from previous_years.test.test_utils import DownloadPastYearForecastSetup
#
# class ViewForecastNaturalAccountCodeAAA(DownloadPastYearForecastSetup):
#
#     def check_nac_table(self, table):
#         nac_rows = table.find_all("tr")
#         first_nac_cols = nac_rows[2].find_all("td")
#         assert (
#             first_nac_cols[0].get_text().strip() == self.nac2_obj.natural_account_code_description  # noqa
#         )
#
#         assert first_nac_cols[3].get_text().strip() == format_forecast_figure(
#             self.budget
#         )
#
#         last_nac_cols = nac_rows[-1].find_all("td")
#         # Check the total for the year
#         assert last_nac_cols[TOTAL_COLUMN].get_text().strip() == \
#             format_forecast_figure(self.year_total)
#         # Check the difference between budget and year total
#         assert last_nac_cols[UNDERSPEND_COLUMN].get_text().strip() == \
#             format_forecast_figure(self.underspend_total)
#         # Check the spend to date
#         assert last_nac_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
#             format_forecast_figure(self.spend_to_date_total)
#
#     def check_negative_value_formatted(self, soup, lenght):
#         negative_values = soup.find_all("span", class_="negative")
#         assert len(negative_values) == lenght
#
#     def check_response(self, resp):
#         self.assertEqual(resp.status_code, 200)
#         self.assertContains(resp, "govuk-table")
#
#         soup = BeautifulSoup(resp.content, features="html.parser")
#
#         # Check that there is 1 table
#         tables = soup.find_all("table", class_="govuk-table")
#         assert len(tables) == 1
#
#         # Check that all the subtotal hierachy_rows exist
#         table_rows = soup.find_all("tr", class_="govuk-table__row")
#         assert len(table_rows) == 4
#
#         self.check_negative_value_formatted(soup, 6)
#
#         # Check that the only table displays the nac and the correct totals
#         self.check_nac_table(tables[0])
#
#     def test_view_cost_centre_nac_details(self):
#         resp = self.factory_get(
#             reverse(
#                 "expenditure_details_cost_centre",
#                 kwargs={
#                     'cost_centre_code': self.cost_centre_code,
#                     'expenditure_category': self.expenditure_id,
#                     'budget_type': self.budget_type,
#                     "period": self.archived_year,
#                 },
#             ),
#             CostCentreExpenditureDetailsView,
#             cost_centre_code=self.cost_centre_code,
#             expenditure_category=self.expenditure_id,
#             budget_type=self.budget_type,
#             period=self.archived_year,
#
#         )
#         self.check_response(resp)
#
#     def test_view_directory_nac_details(self):
#         resp = self.factory_get(
#             reverse(
#                 "expenditure_details_directorate",
#                 kwargs={
#                     'directorate_code': self.directorate.directorate_code,
#                     'expenditure_category': self.expenditure_id,
#                     'budget_type': self.budget_type,
#                     "period": self.archived_year,
#                 },
#             ),
#             DirectorateExpenditureDetailsView,
#             directorate_code=self.directorate.directorate_code,
#             expenditure_category=self.nac1_obj.expenditure_category_id,
#             budget_type=self.budget_type,
#             period=self.archived_year,
#         )
#         self.check_response(resp)
#
#     def test_view_group_nac_details(self):
#         resp = self.factory_get(
#             reverse(
#                 "expenditure_details_group",
#                 kwargs={
#                     'group_code': self.group.group_code,
#                     'expenditure_category': self.expenditure_id,
#                     'budget_type': self.budget_type,
#                     "period": self.archived_year,
#                 },
#             ),
#             GroupExpenditureDetailsView,
#             group_code=self.group.group_code,
#             expenditure_category=self.nac1_obj.expenditure_category_id,
#             budget_type=self.budget_type,
#             period=self.archived_year,
#         )
#
#         self.check_response(resp)
#
#     def test_view_dit_nac_details(self):
#         resp = self.factory_get(
#             reverse(
#                 "expenditure_details_dit",
#                 kwargs={
#                     'expenditure_category': self.expenditure_id,
#                     'budget_type': self.budget_type,
#                     "period": self.archived_year,
#                 },
#             ),
#             DITExpenditureDetailsView,
#             expenditure_category=self.nac1_obj.expenditure_category_id,
#             budget_type=self.budget_type,
#             period=self.archived_year,
#         )
#
#         self.check_response(resp)
#
#
