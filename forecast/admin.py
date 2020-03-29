from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from core.admin import (
    AdminEditOnly,
    AdminImportExport,
    AdminReadOnly,
)

from forecast.import_csv import import_adi_file_class
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialPeriod,
    ForecastEditOpenState,
    ForecastMonthlyFigure,
    UnlockedForecastEditors,
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


class ForecastEditOpenStateAdmin(AdminEditOnly, SimpleHistoryAdmin):
    history_list_display = ["locked"]


class UnlockedForecastEditorsAdmin(admin.ModelAdmin):
    pass


admin.site.register(ForecastMonthlyFigure, MonthlyFigureAdmin)
admin.site.register(FinancialPeriod, FinancialPeriodAdmin)
admin.site.register(BudgetMonthlyFigure, BudgetAdmin)
admin.site.register(ForecastEditOpenState, ForecastEditOpenStateAdmin)
admin.site.register(UnlockedForecastEditors, UnlockedForecastEditorsAdmin)
