from django.core.management.base import BaseCommand

from forecast.models import ForecastMonthlyFigure


class Command(BaseCommand):
    help = "Remove all forecast data"

    def handle(self, *args, **options):
        try:
            ForecastMonthlyFigure.objects.all().delete()
        except Exception as ex:
            self.stdout.write(
                self.style.ERROR(
                    f"Error executing forecast deletion: {ex}"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                "All forecast objects deleted"
            )
        )
