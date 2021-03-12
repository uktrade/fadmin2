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
    help = "Change the actual load flag for the new financial year."

    def handle(self, *args, **options):
        try:

            
                FinancialPeriod.objects.filter(
                    financial_period_code__gte=period_code
                ).update(actual_loaded=False)
                FinancialPeriod.objects.filter(
                    financial_period_code__lt=period_code
                ).update(actual_loaded=True)
                msg = f"Actual flag cleared up to {month_name}"
             self.stdout.write(self.style.SUCCESS(msg))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"An error occured: {ex}"))
