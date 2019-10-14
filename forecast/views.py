import json
from core.views import FidoExportMixin

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

from django_tables2 import MultiTableMixin, SingleTableView
from django_tables2 import RequestConfig

from .models import MonthlyFigure, FinancialPeriod
from .tables import ForecastSubTotalTable, ForecastTable
from .forms import (
    EditForm,
    AddForecastRowForm,
)
from forecast.models import MonthlyFigure
from django.core import serializers
import json

from django.core.serializers.json import DjangoJSONEncoder

# programme__budget_type_fk__budget_type_display indicates if DEL, AME, ADMIN used in every view
budget_type_columns = {
    'programme__budget_type_fk__budget_type_display': 'Budget_type',
    'cost_centre__cost_centre_code': 'Cost Centre Code',
    'cost_centre__cost_centre_name': 'Cost Centre Description',
}

programme_columns = {
    'programme__budget_type_fk__budget_type_display': 'Hidden',
    'natural_account_code__account_L5_code__economic_budget_code': 'Expenditure Type',
    'programme__programme_code': 'Programme Code',
    'programme__programme_description': 'Programme Description'
}

natural_account_columns = {
    'programme__budget_type_fk__budget_type_display': 'Hidden',
    'natural_account_code__expenditure_category__NAC_category__NAC_category_description': 'Budget Grouping',
    'natural_account_code__expenditure_category__grouping_description': 'Budget Category',
}


class PivotClassView(FidoExportMixin, SingleTableView):
    template_name = 'forecast/forecast.html'
    sheet_name = 'Forecast'
    filterset_class = None
    table_class = ForecastTable

    table_pagination = False

    def get_table_kwargs(self):
        return {
            'column_dict': self.column_dict
        }

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it requires the current year, so it is recall each
        # time. Maybe an overkill, but I don't want to risk to forget to change the year!
        d1 = {'cost_centre__directorate__group': 'Group',
              'cost_centre__directorate__group__group_name': 'Name'}
        q = MonthlyFigure.pivot.pivotdata(d1.keys())
        self.queryset = q
        self.column_dict = d1
        super().__init__(*args, **kwargs)


class CostClassView(FidoExportMixin, SingleTableView):
    template_name = 'forecast/forecast.html'
    sheet_name = 'Forecast'
    filterset_class = None
    table_class = ForecastTable
    table_pagination = False

    def get_table_kwargs(self):
        return {
            'column_dict': self.column_dict
        }

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it requires the current year, so it is recall each
        # time. Maybe an overkill, but I don't want to risk to forget to change the year!
        columns = {'cost_centre__cost_centre_code': 'Cost Centre Code',
                   'cost_centre__cost_centre_name': 'Cost Centre Description',
                   'natural_account_code__natural_account_code': 'Natural Account Code',
                   'natural_account_code__natural_account_code_description': 'Natural Account Code Description',
                   'programme__programme_code': 'Programme Code',
                   'programme__programme_description': 'Programme Description',
                   'project_code__project_code': 'Project Code',
                   'project_code__project_description': 'Project Description',
                   'programme__budget_type_fk__budget_type_display': 'Budget Type',
                   'natural_account_code__expenditure_category__NAC_category__NAC_category_description': 'Budget Grouping',
                   'natural_account_code__expenditure_category__grouping_description': 'Budget Category',
                   'natural_account_code__account_L5_code__economic_budget_code': 'Expenditure Type',
                   }
        cost_centre_code = 888812
        pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}
        q = MonthlyFigure.pivot.pivotdata(columns.keys(), pivot_filter)
        self.queryset = q
        self.column_dict = columns
        super().__init__(*args, **kwargs)


class MultiforecastView(MultiTableMixin, TemplateView):
    template_name = 'forecast/forecastmulti.html'

    # table_pagination = {
    #     'per_page': 30
    # }
    table_pagination = False

    def __init__(self, *args, **kwargs):
        # TODO remove hardcoded cost centre
        # TODO Add a field to the chart of account tables specifying the row display order
        # TODO the filter will be set from the request
        cost_centre_code = 888812
        order_list = ['programme__budget_type_fk__budget_type_display_order']
        pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}

        sub_total_type = ['programme__budget_type_fk__budget_type_display']
        display_sub_total_column = 'cost_centre__cost_centre_name'
        q1 = MonthlyFigure.pivot.subtotal_data(display_sub_total_column, sub_total_type,
                                               budget_type_columns.keys(),pivot_filter, order_list = order_list)
        # subtotal_data
        order_list = ['programme__budget_type_fk__budget_type_display_order','natural_account_code__account_L5_code__economic_budget_code']
        sub_total_prog = ['programme__budget_type_fk__budget_type_display',
                    'natural_account_code__account_L5_code__economic_budget_code']
        display_sub_total_column = 'programme__programme_description'
        q2 = MonthlyFigure.pivot.subtotal_data(display_sub_total_column, sub_total_prog, programme_columns.keys(),pivot_filter, order_list = order_list)

        sub_total_nac = ['programme__budget_type_fk__budget_type_display',
                    'natural_account_code__expenditure_category__NAC_category__NAC_category_description']
        display_sub_total_column = 'natural_account_code__expenditure_category__grouping_description'

        q3 = MonthlyFigure.pivot.subtotal_data(display_sub_total_column, sub_total_nac,
                                                natural_account_columns.keys(),pivot_filter, order_list = order_list)
        self.tables = [
            ForecastSubTotalTable(budget_type_columns, q1),
            ForecastSubTotalTable(programme_columns, q2),
            ForecastSubTotalTable(natural_account_columns, q3)
        ]

        super().__init__(*args, **kwargs)


def pivot_test1(request):
    field_dict = {'cost_centre__directorate': 'Directorate',
                  'cost_centre__directorate__directorate_name': 'Name',
                  'natural_account_code': 'NAC'}

    q1 = MonthlyFigure.pivot.pivotdata(field_dict.keys(),
                                       {'cost_centre__directorate__group': '1090AA'})
    table = ForecastTable(field_dict, q1)
    RequestConfig(request).configure(table)
    return render(request, 'forecast/forecast.html', {'table': table})


def add_forecast_row(request):
    cost_centre_code = 888812
    financial_year_id = 2019

    if request.method == 'POST':
        form = AddForecastRowForm(
            request.POST,
        )
        if form.is_valid():
            forecast_row = form.save(commit=False)
            for financial_period in range(1, 13):
                monthly_figure = MonthlyFigure(
                    financial_year_id=financial_year_id,
                    financial_period_id=financial_period,
                    cost_centre_id=cost_centre_code,
                    programme_id=forecast_row.programme_id,
                    natural_account_code_id=forecast_row.natural_account_code_id,
                    analysis1_code_id=forecast_row.analysis1_code_id,
                    analysis2_code_id=forecast_row.analysis2_code_id,
                    amount=0,
                )
                monthly_figure.save()

            return HttpResponseRedirect(
                reverse('edit_forecast')
            )
    else:
        form = AddForecastRowForm()

        gov_select_class = {
            'class': 'govuk-select'
        }
        form.fields['programme'].widget.attrs = gov_select_class
        form.fields['natural_account_code'].widget.attrs = gov_select_class
        form.fields['analysis1_code'].widget.attrs = gov_select_class
        form.fields['analysis2_code'].widget.attrs = gov_select_class
        form.fields['project_code'].widget.attrs = gov_select_class
    return render(
        request,
        'forecast/add.html', {
            'form': form,
            'group': 'Test group',
            'directorate': 'Test directorate',
            'cost_centre_name': 'Test cost centre name',
            'cost_centre_num': cost_centre_code,
        }
    )


def edit_forecast(request):
    field_dict = {
        'cost_centre__directorate': 'Directorate 1',
        # 'cost_centre__directorate__directorate_name': 'Name',
        # 'natural_account_code': 'NAC'
    }

    q1 = MonthlyFigure.pivot.pivotdata(
        field_dict.keys(), {
            'cost_centre__directorate__group': '1090AA'
        }
    )
    table = ForecastTable(field_dict, q1)
    RequestConfig(request).configure(table)

    return render(
        request,
        'forecast/edit.html', {
            'group': "Test group",
            'directorate': "Test directorate",
            'cost_centre_name': "Test cost centre",
            'cost_centre_num': "1090AA",
            'table': table
        }
    )


def edit_forecast_prototype(request):
    financial_year = 2019
    cost_centre_code = "888812"

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            cost_centre_code = form.cleaned_data['cost_centre_code']
            financial_year = form.cleaned_data['financial_year']

            cell_data = json.loads(
                form.cleaned_data['cell_data']
            )

            for key, cell in cell_data.items():
                if cell["editable"]:
                    monthly_figure = MonthlyFigure.objects.filter(
                        cost_centre__cost_centre_code=cost_centre_code,
                        financial_year__financial_year=financial_year,
                        financial_period__period_short_name__iexact=cell["key"],
                        programme__programme_code=cell["programmeCode"],
                        natural_account_code__natural_account_code=cell["naturalAccountCode"],
                    ).first()
                    monthly_figure.amount = int(float(cell["value"]))
                    monthly_figure.save()
    else:
        form = EditForm(
            initial={
                'financial_year': financial_year,
                'cost_centre_code': cost_centre_code
            }
        )
    pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}
    monthly_figures = MonthlyFigure.pivot.pivotdata({}, pivot_filter)

    # TODO - Luisella to restrict to financial year
    editable_periods = list(
        FinancialPeriod.objects.filter(
            actual_loaded=False,
        ).all()
    )

    editable_periods_dump = serializers.serialize(
        "json", editable_periods
    )

    forecast_dump = json.dumps(
        list(monthly_figures),
        cls=DjangoJSONEncoder
    )

    return render(
        request,
        'forecast/edit_prototype.html', {
            'form': form,
            'editable_periods_dump': editable_periods_dump,
            'forecast_dump': forecast_dump,
        }
    )
