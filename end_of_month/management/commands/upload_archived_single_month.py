import csv
import logging
from decimal import Decimal

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from end_of_month.upload_archived_month import (
    WrongArchivePeriodException,
    import_single_archived_period,
)

from forecast.import_csv import WrongChartOFAccountCodeException


class Command(BaseCommand):
    help = "Overwrite a specific month in a specific archive"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("period_upload", type=int)
        parser.add_argument("archive_period", type=int)
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        period = options["period_upload"]
        archive_period = options["archive_period"]
        year = options["financial_year"]

        if period > 15 or period < 1:
            self.stdout.write(self.style.ERROR("Valid Period is between 1 and 15."))
            return

        if archive_period > 15 or archive_period < 1:
            self.stdout.write(
                self.style.ERROR("Valid archive Period is between 1 and 15.")
            )
            return

        # Windows-1252 or CP-1252, used because of a back quote
        csvfile = open(path, newline="", encoding="cp1252")

        try:
            import_single_archived_period(csvfile, period, archive_period, year)
        except (WrongChartOFAccountCodeException, WrongArchivePeriodException) as ex:
            raise CommandError(f"Failure uploading forecast period: {str(ex)}")
            csvfile.close()
            return

        csvfile.close()
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated figures for period {period} "
                f"in archive for period {archive_period}"
            )
        )
