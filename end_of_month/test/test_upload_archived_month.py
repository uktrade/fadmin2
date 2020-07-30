from io import StringIO

from django.test import TestCase

from end_of_month.test.test_utils import SetFullYearArchive
from end_of_month.upload_archived_month import (
    WrongArchivePeriodException,
    import_single_archived_period,
)

from core.test.test_base import RequestFactoryBase


class UploadSingleMonthTest(TestCase, RequestFactoryBase):

    def setUp(self):
        RequestFactoryBase.__init__(self)
        # Archive April, May and June
        self.init_data = SetFullYearArchive(3)

    def test_correct_upload(self):
        pass

    def test_archive_period_errors(self):
        in_mem_csv = StringIO(
            "cost centre,programme,natural account,analysis,analysis2,project,July\n"
            "1,3,4,5,6,7,8\n"
        )
        with self.assertRaises(WrongArchivePeriodException):
            import_single_archived_period(in_mem_csv, 2, 3, 2020)

        with self.assertRaises(WrongArchivePeriodException):
            import_single_archived_period(in_mem_csv, 10, 7, 2020)

    def test_chart_of_account_error(self):
        in_mem_csv = StringIO(
            "cost centre,programme,natural account,analysis,analysis2,project,July\n"
            "1,3,4,5,6,7,8\n"
        )
        with self.assertRaises(WrongArchivePeriodException):
            import_single_archived_period(in_mem_csv, 3, 2, 2020)


