import os

from django.core.management.base import (
    CommandError,
)

from core.command_utils import (
    CommandUpload,
)

from end_of_month.upload_archived_month import (
    WrongArchivePeriodException,
)

from forecast.import_csv import WrongChartOFAccountCodeException

from previous_years.import_previous_year import upload_previous_year_from_file

class Command(CommandUpload):
    help = "Upload a full year of actuals"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        year = options["financial_year"]

        file_name = self.path_to_upload(path, 'xlsx')
        datafile = open(file_name, newline="", encoding="cp1252")

        try:
            upload_previous_year_from_file(datafile, year)
        except (WrongChartOFAccountCodeException, WrongArchivePeriodException) as ex:
            raise CommandError(f"Failure uploading historical actuals: {str(ex)}")
            datafile.close()
            return

        datafile.close()
        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(
            self.style.SUCCESS(
                f"Uploaded historical actuals for year {year} "
            )
        )
