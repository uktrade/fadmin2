from django.core.management.base import BaseCommand

from end_of_month.utils import InvalidPeriodError


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
        parser.add_argument("period", type=int)
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Set the Actual uploaded status from "
            "the beginning of the financial year until and including the given period."
            "Using --clear clear the Actual uploaded status from the given period "
            "until the end of the financial year. "
            "the argument 'period' is the financial period code "
            "(1 for April, 2 for May, etc.) ",
        )

    def handle(self, *args, **options):
        try:
            month_code = options["month_code"]
            if month_code > MAX_PERIOD_CODE or month_code < 0:
                self.stdout.write(
                    self.style.ERROR("Valid Period is between 1 and {MAX_PERIOD_CODE}.")
                )
                return
            financial_period_obj = FinancialPeriod.objects.get(
                period_calendar_code=month_code
            )
            financial_period_code = financial_period_obj.financial_period_code
            month_name = financial_period_obj.period_long_name
            if options["clear"]:
                FinancialPeriod.objects.filter(
                    financial_period_code__gte=financial_period_code
                ).update(actual_loaded=False)
                FinancialPeriod.objects.filter(
                    financial_period_code__lt=financial_period_code
                ).update(actual_loaded=True)
                msg = f"Actual flag cleared up to {month_name}"
            else:
                FinancialPeriod.objects.filter(
                    financial_period_code__lte=financial_period_code
                ).update(actual_loaded=True)
                FinancialPeriod.objects.filter(
                    financial_period_code__gt=financial_period_code
                ).update(actual_loaded=False)

                msg = f"Actual flag set up to {month_name}"
            self.stdout.write(self.style.SUCCESS(msg))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"An error occured: {ex}"))
