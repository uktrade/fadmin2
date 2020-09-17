import csv

from io import StringIO

from bs4 import BeautifulSoup

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    ProgrammeCodeFactory,
)
from chartofaccountDIT.views import (
    HistoricalFilteredProgrammeView,
)

from core.test.test_base import RequestFactoryBase
from core.utils.generic_helpers import get_current_financial_year


class UploadArchiveAnalysis1Test(TestCase, RequestFactoryBase):
    def correct_data_test(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # redefine the header. So, if the object key is changed, this test may fail.
        header_list = ['Analysis 1 Code',
                       'Contract Name',
                       'Supplier',
                       'PC Reference']

        data_list = ['00012',
                       'Test Contract',
                       'Test Supplier',
                       'Test PC Reference']

        csvfile = StringIO.StringIO()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header_list)
        csvwriter.writerow(data_list)
        print(csvfile)