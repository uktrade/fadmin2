from django.test import TestCase

from chartofaccountDIT.import_archived_from_csv import (
    import_archived_analysis1,
    import_archived_analysis2,
)
from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
)

from core.test.test_base import RequestFactoryBase

from forecast.import_csv import WrongChartOFAccountCodeException


class UploadArchiveAnalysis1Test(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # define the header here. So, if the object key is changed, this test may fail.
        header_row = "Analysis 1 Code,Contract Name,Supplier,PC Reference"
        data_row = "00012,Test Contract,Test Supplier,Test PC Reference"

        assert ArchivedAnalysis1.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_analysis1(csvfile, 2019)
        assert ArchivedAnalysis1.objects.all().count() == 1

    def test_wrong_header(self):
        header_row = "Analysis,Contract Name,Supplier,PC Reference"
        data_row = "00012,Test Contract,Test Supplier,Test PC Reference"

        assert ArchivedAnalysis1.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_analysis1(csvfile, 2019)
        assert ArchivedAnalysis1.objects.all().count() == 0


class UploadArchiveAnalysis2Test(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # define the header here. So, if the object key is changed, this test may fail.
        header_row = "Market Code,Market Description"
        data_row = "00012,NeverLand"

        assert ArchivedAnalysis2.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_analysis2(csvfile, 2019)
        assert ArchivedAnalysis2.objects.all().count() == 1

    def test_wrong_header(self):
        header_row = "Market Code,Description"
        data_row = "00012,NeverLand"

        assert ArchivedAnalysis2.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_analysis2(csvfile, 2019)
        assert ArchivedAnalysis2.objects.all().count() == 0
