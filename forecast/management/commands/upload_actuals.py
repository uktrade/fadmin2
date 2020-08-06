import os

from core.command_utils import (
    CommandUpload,
)

from forecast.import_actuals import upload_trial_balance_report


class Command(CommandUpload):
    help = "Upload the Trial Balance for a specific month"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("month", type=int)
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        month = options["month"]
        year = options["financial_year"]
        file_name = self.path_to_upload(path, 'xslx')
        upload_trial_balance_report(file_name, month, year)
        if self.upload_s3:
            os.remove(file_name)

        self.stdout.write(
            self.style.SUCCESS(
                "Actual for period {} added".format(
                    month
                )
            )
        )
