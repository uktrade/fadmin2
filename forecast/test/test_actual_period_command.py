from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from forecast.models import FinancialPeriod


class GiftsHospitalityCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def set_all_actual(self):
        FinancialPeriod.objects.all().update(actual_loaded=True)

    def clear_all_actual(self):
        FinancialPeriod.objects.all().update(actual_loaded=False)

    def test_clear_all_actuals(self):
        self.set_all_actual()
        self.assertEqual (
            FinancialPeriod.objects.filter(actual_loaded=False).count(),
            15
        )
        call_command(
            "set_actual_period", "--clear", month=4, stdout=self.out
        )
        self.assertEqual (
            FinancialPeriod.objects.filter(actual_loaded=False).count(),
            0
        )


