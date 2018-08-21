import django_tables2 as tables
from .models import NaturalCode

from core.tables import FadminTable


class NaturalCodeTable(FadminTable):

    nac_category_description = tables.Column(verbose_name='Budget Grouping', accessor='NAC_category.NAC_category_description')
    budget_description = tables.Column(verbose_name='Expenditure Category', accessor='dashboard_grouping.grouping_description')
    budget_NAC_code = tables.Column(verbose_name='NAC for Budget/Forecast', accessor='dashboard_grouping.linked_budget_code.natural_account_code')
    budget_NAC_description = tables.Column(verbose_name='Description', accessor='dashboard_grouping.linked_budget_code.natural_account_code_description')
    account_L5_code__economic_budget_code = tables.Column(verbose_name='Expenditure Type', accessor ='account_L5_code.economic_budget_code')
    natural_account_code = tables.Column(verbose_name='NAC')
    natural_account_code_description = tables.Column(verbose_name='Description')

    class Meta(FadminTable.Meta):
        model = NaturalCode
        fields = ('account_L5_code__economic_budget_code',
                  'nac_category_description',
                  'budget_description',
                  'budget_NAC_code',
                  'budget_NAC_description',
                  'natural_account_code',
                  'natural_account_code_description',
                  )


