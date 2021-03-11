from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core.utils.command_helpers import get_no_answer
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_year_display,
)

from end_of_month.models import (
    EndOfMonthStatus,
    MonthlyTotalBudget,
)

from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    ForecastMonthlyFigure,
)

from previous_years.models import ArchivedFinancialCode


class Command(BaseCommand):
    help = "Delete all forecast/actual/budget figures from the current year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Tells Django to NOT prompt the user for input of any kind.",
        )

    def handle(self, *args, **options):
        self.interactive = options["interactive"]
        current_year = get_current_financial_year()
        current_year_display = get_year_display(current_year)
        error_message = (
            f"forecast/actual/budget figures "
            f"for {current_year_display} not deleted."
        )

        if not ArchivedFinancialCode.objects.filter(
            financial_year=current_year
        ).count():
            # If the archive does not exists, ask the users if they want to proceed.
            # If we are not asking questions, consider it a fatal error and exit.
            if self.interactive:
                prompt = (
                    f"The figures for the financial year {current_year_display} "
                    f"are not archived.\n"
                )
                self.stdout.write(self.style.WARNING(prompt))
                abort = get_no_answer()
            else:
                abort = True
                error_message = (
                    f"ABORT (--noinput) - forecast/actual/budget figures "
                    f"for {current_year_display} not deleted."
                )

            if abort:
                self.stdout.write(self.style.ERROR(error_message))
                raise CommandError(error_message)
                return

        if self.interactive:
            prompt = (
                f"All the forecast/actual/budget figures "
                f"for {current_year_display} will be deleted.\n"
                f"This operation cannot be undone.\n"
            )

            self.stdout.write(self.style.WARNING(prompt))
            if get_no_answer():
                self.stdout.write(self.style.ERROR(error_message))
                raise CommandError(error_message)
                return

        self.stdout.write(self.style.WARNING("Deleting budget figures...."))
        BudgetMonthlyFigure.objects.filter(financial_year=current_year).delete()
        BudgetMonthlyFigure.objects.filter(financial_year__isnull=True).delete()
        MonthlyTotalBudget.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Budget figures deleted."))

        self.stdout.write(self.style.WARNING("Deleting forecast/actual figures...."))
        ForecastMonthlyFigure.objects.filter(financial_year=current_year).delete()
        ForecastMonthlyFigure.objects.filter(financial_year__isnull=True).delete()
        EndOfMonthStatus.objects.all().update(
            archived = False,
            archived_by = None,
            archived_date = None,
        )
        FinancialCode.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"forecast/actual/budget figures for for {current_year_display} "
                f"deleted."
            )
        )
