import os
from copy import deepcopy
from datetime import datetime
from unittest.mock import MagicMock, patch
from zipfile import BadZipFile

from openpyxl.utils.cell import get_column_letter

from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.db.models import Sum
from django.test import (
    RequestFactory,
    TestCase,
    override_settings,
)

from chartofaccountDIT.test.factories import (
    HistoricalAnalysis1Factory,
    HistoricalAnalysis2Factory,
    HistoricalNaturalCodeFactory,
    HistoricalProgrammeCodeFactory,
    HistoricalProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import RequestFactoryBase
from core.utils.excel_test_helpers import (
    FakeCell,
    FakeWorkSheet
)

from costcentre.test.factories import (
    ArchivedCostCentreFactory,
)

from previous_years.import_previous_year import (
    EXPECTED_CHART_OF_ACCOUNT_HEADERS,
    MONTH_HEADERS,
)

class ImportPreviousYearForecastTest(TestCase, RequestFactoryBase):

    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.factory = RequestFactory()
        # 2019 is created when the database is created
        self.archived_year = 2019
        self.archived_year_obj = \
            FinancialYear.objects.get(pk=self.archived_year)
        self.cost_centre_code = "109189"
        self.natural_account_code = 52191003
        self.programme_code = "310940"
        self.project_code = "0123"
        self.analisys1 = "00798"
        self.analisys2 = "00321"
        ArchivedCostCentreFactory.create(
            cost_centre_code=self.cost_centre_code,
            financial_year=self.archived_year_obj
        )
        HistoricalProjectCodeFactory.create(
            project_code=self.project_code,
            financial_year=self.archived_year_obj
        )
        HistoricalProgrammeCodeFactory.create(
            programme_code=self.programme_code,
            financial_year=self.archived_year_obj
        )
        HistoricalNaturalCodeFactory.create(
            natural_account_code=self.natural_account_code,
            economic_budget_code="CAPITAL",
            financial_year=self.archived_year_obj
        )
        HistoricalAnalysis2Factory.create(
            analysis2_code=self.analisys2,
            financial_year=self.archived_year_obj
        )
        HistoricalAnalysis1Factory.create(
            analysis1_code=self.analisys1,
            financial_year=self.archived_year_obj
        )

    def set_worksheet_header(self):
        self.fake_work_sheet = FakeWorkSheet()
        self.fake_work_sheet.title = "Previous_Years"
        col_index = 0
        for item in EXPECTED_CHART_OF_ACCOUNT_HEADERS:
            col_index += 1
            cell_index = f"{get_column_letter(col_index)}1"
            self.fake_work_sheet[cell_index] = FakeCell(item)

        for month in MONTH_HEADERS:
            col_index += 1
            cell_index = f"{get_column_letter(col_index)}1"
            self.fake_work_sheet[cell_index] = FakeCell(month)

    def test_upload_previous_year(self):
        self.set_worksheet_header()