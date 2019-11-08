from django.test import RequestFactory, TestCase

import os

from typing import (
    TypeVar, Dict,
)

from zipfile import BadZipFile

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear

from costcentre.test.factories import CostCentreFactory

from forecast.import_actuals import (
    CORRECT_TITLE,
    MONTH_CELL,
    TITLE_CELL,
    TrialBalanceError,
    VALID_ECONOMIC_CODE_LIST,
    check_trial_balance_format,
    save_row,
    upload_trial_balance_report,
    GENERIC_PROGRAMME_CODE
)
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)

from upload_file.models import FileUpload

TEST_COST_CENTRE = 109189
TEST_VALID_NATURAL_ACCOUNT_CODE = 52191003
TEST_PROGRAMME_CODE = '310940'

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class FakeWorkSheet(Dict[_KT, _VT]):
    title = None


class FakeCell:
    value = None

    def __init__(self, value):
        self.value = value


class ImportActualsTest(TestCase):
    def setUp(self):
        self.test_year = 2019
        self.test_period = 4

        self.factory = RequestFactory()
        self.cost_centre_code = TEST_COST_CENTRE
        self.valid_natural_account_code = TEST_VALID_NATURAL_ACCOUNT_CODE
        self.programme_code = TEST_PROGRAMME_CODE
        self.test_amount = 100
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        NaturalCodeFactory.create(
            natural_account_code=self.valid_natural_account_code,
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0]
        )
        ProgrammeCodeFactory.create(
            programme_code=self.programme_code
        )
        self.period_obj = FinancialPeriod.objects.get(financial_period_code=2)
        self.year_obj = FinancialYear.objects.get(financial_year=2019)

        self.chart_of_account_line_correct = \
        '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
            self.cost_centre_code,
            self.valid_natural_account_code,
            self.programme_code
        )

        self.chart_of_account_line_no_programme = \
        '3000-30000-{}-{}-000000-00000-00000-0000-0000-0000'.format(
            self.cost_centre_code,
            self.valid_natural_account_code,
         )

    def test_save_row(self):
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        save_row(
            self.chart_of_account_line_correct,
            self.test_amount,
            self.period_obj,
            self.year_obj,
        )

        self.assertEqual(
            MonthlyFigure.objects.filter(cost_centre=self.cost_centre_code).count(),
            1,
        )
        q = MonthlyFigure.objects.get(cost_centre=self.cost_centre_code)
        self.assertEqual(
            q.amount,
            self.test_amount * 100,
        )

        save_row(
            self.chart_of_account_line_correct,
            self.test_amount * 2,
            self.period_obj,
            self.year_obj,
        )
        # check that lines with the same chart of account are added together
        self.assertEqual(
            MonthlyFigure.objects.filter(cost_centre=self.cost_centre_code).count(),
            1,
        )
        q = MonthlyFigure.objects.get(cost_centre=self.cost_centre_code)
        self.assertEqual(
            q.amount,
            self.test_amount * 100 * 3,
        )

    def test_save_row_no_programme(self):
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        save_row(
            self.chart_of_account_line_no_programme,
            0,
            self.period_obj,
            self.year_obj,
        )
        # Lines with 0 programme and 0 amount are not saved
        self.assertEqual(
            MonthlyFigure.objects.filter(cost_centre=self.cost_centre_code).count(),
            0,
        )

        save_row(
            self.chart_of_account_line_no_programme,
            self.test_amount,
            self.period_obj,
            self.year_obj,
        )
        # check that the line has been saved
        self.assertEqual(
            MonthlyFigure.objects.filter(cost_centre=self.cost_centre_code).count(),
            1,
        )
        q = MonthlyFigure.objects.get(cost_centre=self.cost_centre_code)
        self.assertEqual(
            q.amount,
            self.test_amount * 100
        )
        self.assertEqual(
            int(q.programme.programme_code),
            GENERIC_PROGRAMME_CODE
        )




    def test_upload_trial_balance_report(self):
        # Check that BadZipFile is raised on
        # supply of incorrect file format
        # with self.assertRaises(BadZipFile):
        #     upload_trial_balance_report(None, 1, 1)

        bad_title_file_path = os.path.join(
            os.path.dirname(__file__),
            'test_assets/bad_title_upload_test.xlsx',
        )

        bad_title_file_upload = FileUpload(
            document_file=bad_title_file_path
        )
        bad_title_file_upload.save()

        with self.assertRaises(TrialBalanceError):
            upload_trial_balance_report(
                bad_title_file_upload,
                self.test_year,
                self.test_period,
            )

        # Create monthly figure - check this is deleted after func called

        # test_file_path = os.path.join(
        #     os.path.dirname(__file__),
        #     'test_assets/upload_test.xlsx',
        # )
        #
        # test_file_upload = FileUpload(
        #     document_file=test_file_path
        # )
        # test_file_upload.save()
        #
        # upload_trial_balance_report(
        #     test_file_upload,
        #     self.test_year,
        #     self.test_period,
        # )

        # Check for existence of monthly figures

        # Check that figures have correct values

    def check_trial_balance_format(self):
        fake_work_sheet = FakeWorkSheet()
        fake_cell = FakeCell("test")

        fake_work_sheet[TITLE_CELL] = fake_cell

        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                1,
                1,
            )
