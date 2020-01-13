from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from core.admin import (
    AdminImportExport,
    AdminReadOnly,
)

from forecast.import_csv import import_adi_file_class
from forecast.models import (
    Budget,
    FinancialPeriod,
    MonthlyFigure,
)


class MonthlyFigureAdmin(AdminImportExport, AdminReadOnly, SimpleHistoryAdmin):
    @property
    def import_info(self):
        return import_adi_file_class


class BudgetAdmin(AdminReadOnly):
    pass


class FinancialPeriodAdmin(AdminReadOnly):
    list_display = (
        "period_short_name",
        "period_long_name",
        "financial_period_code",
        "period_calendar_code",
        "actual_loaded",
        "display_figure"
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "period_short_name",
                "period_long_name",
                "financial_period_code",
                "period_calendar_code",
            ]


admin.site.register(MonthlyFigure, MonthlyFigureAdmin)
admin.site.register(FinancialPeriod, FinancialPeriodAdmin)
admin.site.register(Budget, BudgetAdmin)
