from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from core.admin import AdminActiveField, AdminExport, AdminImportExport, AdminreadOnly
from core.exportutils import generic_table_iterator, export_to_excel, \
    generic_export_to_csv, generic_export_to_excel

from .importcsv import import_Analysis1, import_Analysis2, import_commercial_category, import_NAC, \
    import_NAC_dashboard_Budget, import_NAC_category, import_programme

from .models import Analysis1, Analysis2, CommercialCategory, ExpenditureCategory, \
    NACCategory, NaturalCode, ProgrammeCode


def _export_nac_iterator(queryset):
    yield ['Level 6', 'Level 6 Description',
           'Active', 'Level 5', 'Level 5 Description',
           'Category', 'Dashboard Group']

    for obj in queryset:
        yield [obj.natural_account_code,
               obj.natural_account_code_description,
               obj.active,
               obj.account_L5_code.account_l5_code,
               obj.account_L5_code.account_l5_long_name]


class NaturalCodeAdmin(AdminreadOnly, AdminImportExport):
    list_display = ('natural_account_code', 'natural_account_code_description', 'active')

    def get_readonly_fields(self, request, obj=None):
        return ['natural_account_code', 'natural_account_code_description', 'account_L5_code']

    def get_fields(self, request, obj=None):
        return ['natural_account_code', 'natural_account_code_description',
                'account_L5_code', 'expenditure_category',
                'commercial_category', 'used_for_budget', 'active']

    search_fields = ['natural_account_code', 'natural_account_code_description']
    list_filter = ('active',
                   'used_for_budget',
                   ('expenditure_category__NAC_category', RelatedDropdownFilter),
                   ('expenditure_category', RelatedDropdownFilter))
    @property
    def export_func(self):
        return _export_nac_iterator

    @property
    def import_func(self):
        return import_NAC


class Analysis1Admin(AdminreadOnly, AdminActiveField,  AdminImportExport):
    search_fields = ['analysis1_description', 'analysis1_code']
    list_display = ('analysis1_code', 'analysis1_description', 'active')

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_func(self):
        return import_Analysis1


class Analysis2Admin(AdminreadOnly,  AdminActiveField, AdminImportExport):
    search_fields = ['analysis2_description', 'analysis2_code']
    list_display = ('analysis2_code', 'analysis2_description', 'active')

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_func(self):
        return import_Analysis2



class ExpenditureCategoryAdmin(AdminImportExport):
    search_fields = ['grouping_description', 'description']
    list_display = ['grouping_description', 'description', 'NAC_category', 'linked_budget_code']
    list_filter = ('NAC_category',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "linked_budget_code":
            kwargs["queryset"] = NaturalCode.objects.filter(used_for_budget=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_func(self):
        return import_NAC_category


def export_NACCategory_csv(modeladmin, request, queryset):
    return (generic_export_to_csv(queryset))


def export_NACCategory_xlsx(modeladmin, request, queryset):
    return (generic_export_to_excel(queryset))


class NACCategoryAdmin(admin.ModelAdmin):
    actions = [export_NACCategory_csv, export_NACCategory_xlsx]


def _export_programme_iterator(queryset):
    yield ['Programme Code', 'Description', 'Budget Type', 'Active']
    for obj in queryset:
        yield [obj.programme_code,
               obj.programme_description,
               obj.budget_type,
               obj.active]


class ProgrammeAdmin(AdminActiveField, AdminImportExport):
    list_display = ('programme_code', 'programme_description', 'budget_type', 'active')
    search_fields = ['programme_code', 'programme_description']
    list_filter = ['budget_type', 'active']

    def get_readonly_fields(self, request, obj=None):
        return ['programme_code', 'programme_description', 'budget_type', 'created',
                'updated']  # don't allow to edit the code

    def get_fields(self, request, obj=None):
        return ['programme_code', 'programme_description',
                'budget_type', 'active', 'created', 'updated']

    @property
    def export_func(self):
        return _export_programme_iterator

    @property
    def import_func(self):
        return import_programme


admin.site.register(Analysis1, Analysis1Admin)
admin.site.register(Analysis2, Analysis2Admin)
admin.site.register(NaturalCode, NaturalCodeAdmin)
admin.site.register(ExpenditureCategory, ExpenditureCategoryAdmin)
admin.site.register(NACCategory, NACCategoryAdmin)
admin.site.register(CommercialCategory)
admin.site.register(ProgrammeCode, ProgrammeAdmin)
