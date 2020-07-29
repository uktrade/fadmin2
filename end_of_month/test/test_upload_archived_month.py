import io

from django.test import TestCase

from end_of_month.test.test_utils import SetFullYearArchive

from core.test.test_base import RequestFactoryBase

class UploadSingleMonthTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.archive = SetFullYearArchive()

    def test_correct_upload(self):
        pass

    def test_archive_period_errors(self):
        pass

    def test_chart_of_account_error(self):
        pass