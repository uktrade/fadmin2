from django.core.management.base import BaseCommand

from end_of_month.utils import (
    InvalidPeriodError,
)


from forecast.models import (
    MAX_PERIOD_CODE,
    FinancialPeriod,
)

def validate_period_code(period_code):
    if period_code > MAX_PERIOD_CODE or period_code < 1:
        raise InvalidPeriodError()


class Command(BaseCommand):
    help = "Set or clear the Actual uploaded status"

    def add_arguments(self, parser):
        parser.add_argument("month", type=int)
        # Named (optional) arguments
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear the Actual uploaded status from "
            "the given month to the end of the financial year. "
            "month is the calendar month code (1 for January, 2 for April, etc.)",
        )

    def handle(self, *args, **options):
        try:
            month = options["month"]
            try:
                validate_period_code(month)
            except InvalidPeriodError:
                self.stdout.write(
                    self.style.ERROR("Valid Period is between 1 and {MAX_PERIOD_CODE}.")
                )
                return
            financial_period_obj = FinancialPeriod.objects.get(period_calendar_code=month)
            financial_period_code = financial_period_obj.financial_period_code
            month_name = financial_period_obj.period_long_name
            if options["clear"]:
                FinancialPeriod.objects.filter(
                    financial_period_code__gte=financial_period_code
                ).update(actual_loaded=False)
                msg = "Cleared"
            else:
                FinancialPeriod.objects.filter(
                    financial_period_code__lte=financial_period_code
                ).update(actual_loaded=True)
                msg = "Set"
                self.stdout.write(self.style.SUCCESS(msg))
        except Exception as ex:
            self.stdout.write(
                self.style.ERROR(f"An error occured: {ex}")
            )
