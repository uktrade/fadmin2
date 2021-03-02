from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from forecast.models import (
    MAX_PERIOD_CODE,
    FinancialPeriod,
)


class SetActualPeriodCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def set_all_actual(self):
        FinancialPeriod.objects.all().update(actual_loaded=True)
        self.assertEqual(FinancialPeriod.objects.filter(actual_loaded=False).count(), 0)

    def clear_all_actual(self):
        FinancialPeriod.objects.all().update(actual_loaded=False)
        self.assertEqual(FinancialPeriod.objects.filter(actual_loaded=True).count(), 0)

    def test_clear_all_actuals(self):
        self.set_all_actual()
        call_command("set_actual_period", "--clear", 1, stdout=self.out)
        self.assertEqual(FinancialPeriod.objects.filter(actual_loaded=True).count(), 0)

    def test_set_all_actuals(self):
        self.clear_all_actual()
        call_command("set_actual_period", MAX_PERIOD_CODE, stdout=self.out)
        self.assertEqual(
            FinancialPeriod.objects.filter(actual_loaded=True).count(), MAX_PERIOD_CODE
        )
