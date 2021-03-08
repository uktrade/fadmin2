import os
from django.core.management import call_command
from django.core.management.base import CommandError

from django.test import TestCase

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
    HistoricalAnalysis1Factory,
    HistoricalAnalysis2Factory,
    HistoricalNaturalCodeFactory,
    HistoricalProgrammeCodeFactory,
    HistoricalProjectCodeFactory,
)

from core.models import FinancialYear

from costcentre.test.factories import (
    ArchivedCostCentreFactory,
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)
from end_of_month.test.test_utils import MonthlyFigureSetup

from previous_years.archive_current_year_figure import archive_current_year

from previous_years.models import (
    ArchivedFinancialCode,
    ArchivedForecastData,
)

from previous_years.utils import ArchiveYearError

from upload_file.models import FileUpload


class ArchiveCurrentYearErrorTest(TestCase):
    def setUp(self):
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()

    def test_command_error(self):
        with self.assertRaises(CommandError):
            call_command("archive_current_year",)

    def test_error_no_archived_chart_of_account(self):
        with self.assertRaises(ArchiveYearError):
            archive_current_year()


class ArchiveCurrentYearTest(TestCase):
    def setUp(self):
        self.init_data = MonthlyFigureSetup()
        self.init_data.setup_forecast()
        call_command()

    def test_command_error(self):
        with self.assertRaises(CommandError):
            call_command("archive_current_year",)
