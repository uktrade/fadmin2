from django.core.management.base import BaseCommand

from core.utils.generic_helpers import (
    get_current_financial_year,
    get_year_display,
)

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    ForecastMonthlyFigure,
)

from previous_years.models import ArchivedFinancialCode

def boolean_input(question, default=None):
    result = input("%s " % question)
    if not result and default is not None:
        return default
    while len(result) < 1 or result[0].lower() not in "yn":
        result = input("Please answer yes or no: ")
    return result[0].lower() == "y"


class Command(BaseCommand):
    help = "Delete all forecast/actual/budget figures from the current year"

    def handle(self, *args, **options):
        current_year = get_current_financial_year()
        current_year_display = get_year_display(current_year)

        if not ArchivedFinancialCode.objects.filter(
                financial_year=current_year).count():
            if not boolean_input(
                    f"The figures for the financial year {current_year_display} "
                    f"are not archived.\n"
                    "Do you want to proceed? (y/n)"):
                self.stdout.write(
                    self.style.ERROR(
                        f"forecast/actual/budget figures for for {current_year_display} "
                        f"not deleted"
                    )
                )
                return

        if not boolean_input("This will delete all the forecast/actual/budget figures "
                             f"for {current_year_display}.\n"
                             "This operation cannot be undone.\n"
                             "Do you want to proceed? (y/n)"):
            self.stdout.write(
                self.style.ERROR(
                    f"forecast/actual/budget figures for for {current_year_display} "
                    f"not deleted"
                )
            )
            return

        BudgetMonthlyFigure.objects.filter(financial_year=current_year).delete()
        BudgetMonthlyFigure.objects.filter(financial_year__isnull=True).delete()

        ForecastMonthlyFigure.objects.filter(financial_year=current_year).delete()
        ForecastMonthlyFigure.objects.filter(financial_year__isnull=True).delete()

        FinancialCode.objects.filter(financial_year=current_year).delete()
        FinancialCode.objects.filter(financial_year__isnull=True).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"forecast/actual/budget figures for for {current_year_display} "
                f"deleted."
            )
        )



