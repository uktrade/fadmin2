import os
from datetime import datetime
from typing import (
    Dict,
    TypeVar,
)
from zipfile import BadZipFile

from django.db.models import Sum
from django.test import RequestFactory, TestCase

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear

from costcentre.test.factories import CostCentreFactory

from forecast.import_actuals import (
    CORRECT_TITLE,
    CORRECT_WS_TITLE,
    GENERIC_PROGRAMME_CODE,
    MONTH_CELL,
    TITLE_CELL,
    TrialBalanceError,
    VALID_ECONOMIC_CODE_LIST,
    check_trial_balance_format,
    save_row,
    upload_trial_balance_report,
)
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)

from upload_file.models import FileUpload

TEST_COST_CENTRE = 109189
TEST_VALID_NATURAL_ACCOUNT_CODE = 52191003
TEST_NOT_VALID_NATURAL_ACCOUNT_CODE = 92191003
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
        self.test_period = 9

        self.factory = RequestFactory()
        self.cost_centre_code = TEST_COST_CENTRE
        self.valid_natural_account_code = TEST_VALID_NATURAL_ACCOUNT_CODE
        self.not_valid_natural_account_code = TEST_NOT_VALID_NATURAL_ACCOUNT_CODE
        self.programme_code = TEST_PROGRAMME_CODE
        self.test_amount = 100
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        NaturalCodeFactory.create(
            natural_account_code=self.valid_natural_account_code,
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0]
        )
        NaturalCodeFactory.create(
            natural_account_code=18162001,
            economic_budget_code=VALID_ECONOMIC_CODE_LIST[0]
        )
        NaturalCodeFactory.create(
            natural_account_code=self.not_valid_natural_account_code
        )
        ProgrammeCodeFactory.create(
            programme_code=self.programme_code
        )
        ProgrammeCodeFactory.create(
            programme_code='310540'
        )
        ProgrammeCodeFactory.create(
            programme_code='310530'
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

        self.chart_of_account_line_not_valid_nac = \
            '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.not_valid_natural_account_code,
                self.programme_code
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
        q = MonthlyFigure.objects.get(cost_centre=self.cost_centre_code)

        self.assertEqual(
            q.amount,
            self.test_amount * 100
        )
        self.assertEqual(
            int(q.programme.programme_code),
            GENERIC_PROGRAMME_CODE
        )

    def test_save_row_not_valid_nac(self):
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

        save_row(
            self.chart_of_account_line_not_valid_nac,
            10,
            self.period_obj,
            self.year_obj,
        )

        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )

    def test_upload_trial_balance_report(self):
        # Check that BadZipFile is raised on
        # supply of incorrect file format
        bad_file_type_upload = FileUpload(
            document_file=os.path.join(
                os.path.dirname(__file__),
                'test_assets/bad_file_type.csv', )
        )
        bad_file_type_upload.save()
        with self.assertRaises(BadZipFile):
            upload_trial_balance_report(
                bad_file_type_upload,
                self.test_period,
                self.test_year,
            )

        bad_title_file_upload = FileUpload(
            document_file=os.path.join(
            os.path.dirname(__file__),
            'test_assets/bad_title_upload_test.xlsx',)
        )
        bad_title_file_upload.save()

        with self.assertRaises(TrialBalanceError):
            upload_trial_balance_report(
                bad_title_file_upload,
                self.test_period,
                self.test_year,
            )

        good_file_upload = FileUpload(
            document_file=os.path.join(
            os.path.dirname(__file__),
            'test_assets/upload_test.xlsx',)
        )
        good_file_upload.save()
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            0,
        )
        upload_trial_balance_report(
            good_file_upload,
            self.test_period,
            self.test_year,
        )
        # Check for existence of monthly figures
        self.assertEqual(
            MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).count(),
            4,
        )
        result = MonthlyFigure.objects.filter(
                cost_centre=self.cost_centre_code
            ).aggregate(total = Sum('amount'))

        # Check that figures have correct values
        self.assertEqual(
            result['total'],
            1000000,
        )

    def test_check_trial_balance_format(self):
        fake_work_sheet = FakeWorkSheet()
        fake_work_sheet.title = CORRECT_WS_TITLE
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TITLE)
        fake_work_sheet[MONTH_CELL] = FakeCell(datetime(2019, 8, 1))
        # wrong month
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                9,
                2019,
            )
        #   wrong year
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2018,
            )
        # Wrong title
        fake_work_sheet[TITLE_CELL] = FakeCell('Wrong Title')
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2019,
            )
        # wrong worksheet title
        fake_work_sheet.title = 'Unknown'
        fake_work_sheet[TITLE_CELL] = FakeCell(CORRECT_TITLE)
        with self.assertRaises(TrialBalanceError):
            check_trial_balance_format(
                fake_work_sheet,
                8,
                2019,
            )
