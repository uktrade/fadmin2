from django.contrib import admin

from core.admin import (
    AdminImportExport,
    AdminReadOnly,
)

from forecast.import_csv import import_adi_file_class
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
    FileUpload,
)


class MonthlyFigureAdmin(AdminImportExport, AdminReadOnly):
    @property
    def import_info(self):
        return import_adi_file_class


admin.site.register(MonthlyFigure, MonthlyFigureAdmin)
admin.site.register(FileUpload)
admin.site.register(FinancialPeriod)
