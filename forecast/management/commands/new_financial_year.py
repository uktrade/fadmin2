from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from core.utils.command_helpers import get_no_answer
from core.utils.generic_helpers import (
    create_financial_year_display,
    get_current_financial_year,
    get_year_display,
)


class Command(BaseCommand):
    help = "Run all the operations required to prepare for the new financial year"

    def run_command(self, command_name, message):
        self.stdout.write(self.style.WARNING(f"{message}..."))
        try:
            call_command(command_name)
        except CommandError:
            full_error_message = f"{message} failed. \n {self.error_message}"
            self.stdout.write(self.style.ERROR(full_error_message))
            raise CommandError(full_error_message)
            return False
        return True

    def handle(self, *args, **options):
        current_financial_year = get_current_financial_year()
        current_financial_year_display = get_year_display(current_financial_year)
        new_financial_year = current_financial_year + 1
        new_financial_year_display = get_year_display(new_financial_year)
        self.error_message = (
            f"Financial year {current_financial_year_display} not changed."
        )

        prompt = (
            f"The financial year will change from  "
            f"{current_financial_year_display} to {new_financial_year_display}.\n"
            f"This operation cannot be undone.\n"
        )

        self.stdout.write(self.style.WARNING(prompt))
        if get_no_answer():
            self.stdout.write(self.style.ERROR(self.error_message))
            raise CommandError(self.error_message)
            return


        if not call_command("archive", "Archiving chart of account"):
            return
        if not call_command("archive_current_year", "Archiving forecast/actual/budget"):
            return
        if not call_command("archive", "Archiving chart of account"):
            return
        if not call_command("archive", "Archiving chart of account"):
            return
        if not call_command("archive", "Archiving chart of account"):
            return

        self.stdout.write(self.style.WARNING("..."))
        call_command("archive_current_year")
        self.stdout.write(self.style.WARNING("Deleting forecast/actual/budget..."))
        call_command("clear_forecast", "--noinput")
        self.stdout.write(self.style.WARNING("Set the current financial year to ..."))
        call_command("set_current_year")
        call_command("set_actual_period", "--clear", 1)

        self.stdout.write(
                self.style.SUCCESS(
                    f"FFT ready for  {current_financial_year_display} "
                    f"deleted."
                )
            )
