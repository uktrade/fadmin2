from openpyxl.utils.cell import get_column_letter

from django.test import (
    RequestFactory,
    TestCase,
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
    COST_CENTRE_HEADER,
    NAC_HEADER,
    PROGRAMME_HEADER,
    PROJECT_HEADER,
    ANALYSIS_HEADER,
    ANALYSIS2_HEADER,
    MONTH_HEADERS,
    upload_previous_year,
)

from upload_file.models import FileUpload

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

    def set_cell(self, col_index, row_index, value):
        cell_index = f"{get_column_letter(col_index)}{row_index}"
        self.fake_work_sheet[cell_index] = FakeCell(value)

    def set_worksheet_header(self):
        self.fake_work_sheet = FakeWorkSheet()
        self.fake_work_sheet.title = "Previous_Years"
        col_index = 1
        self.set_cell(col_index, 1, COST_CENTRE_HEADER)
        self.set_cell(col_index, 2, self.cost_centre_code)
        col_index += 1
        self.set_cell(col_index, 1, NAC_HEADER)
        self.set_cell(col_index, 2, self.natural_account_code)
        col_index += 1
        self.set_cell(col_index, 1, PROGRAMME_HEADER)
        self.set_cell(col_index, 2, self.programme_code)
        col_index += 1
        self.set_cell(col_index, 1, PROJECT_HEADER)
        self.set_cell(col_index, 2, self.project_code)
        col_index += 1
        self.set_cell(col_index, 1, ANALYSIS_HEADER)
        self.set_cell(col_index, 2, self.analisys1)
        col_index += 1
        self.set_cell(col_index, 1, ANALYSIS2_HEADER)
        self.set_cell(col_index, 2, self.analisys2)

        for month in MONTH_HEADERS:
            col_index += 1
            self.set_cell(col_index, 1, month)
            self.set_cell(col_index, 2, col_index*13)


    def test_upload_previous_year(self):
        self.set_worksheet_header()
        file_upload_obj = FileUpload(
                document_file_name="dummy.xlxs",
                document_type=FileUpload.PREVIOUSYEAR,
                file_location=FileUpload.LOCALFILE,
        )
        file_upload_obj.save()

        upload_previous_year(
            self.fake_work_sheet,
            self.archived_year,
            file_upload_obj,
        )