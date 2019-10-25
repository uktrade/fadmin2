import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django_tables2 import MultiTableMixin, SingleTableView, RequestConfig

from forecast.models import MonthlyFigure, FinancialPeriod
from forecast.tables import ForecastSubTotalTable, ForecastTable
from forecast.forms import EditForm, AddForecastRowForm
from core.views import FidoExportMixin
from forecast.views.base import (
    ForecastBaseView,
    NoCostCentreCodeInURLError,
)
from costcentre.models import CostCentre


# programme__budget_type_fk__budget_type_display
# indicates if DEL, AME, ADMIN used in every view
budget_type_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget_type",
    "cost_centre__cost_centre_code": "Cost Centre Code",
    "cost_centre__cost_centre_name": "Cost Centre Description",
}

programme_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_description": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_name": "Expenditure Type",
    "programme__programme_code": "Programme Code",
    "programme__programme_description": "Programme Description",
}

natural_account_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping",  # noqa
    "natural_account_code__expenditure_category__grouping_description": "Budget Category",  # noqa
}


class PivotClassView(FidoExportMixin, SingleTableView):
    template_name = "forecast/forecast.html"
    sheet_name = "Forecast"
    filterset_class = None
    table_class = ForecastTable

    table_pagination = False

    def get_table_kwargs(self):
        return {"column_dict": self.column_dict}

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it
        # requires the current year, so it is
        # recall each time. Maybe an overkill,
        # but I don't want to risk to forget
        # to change the year!
        d1 = {
            "cost_centre__directorate__group": "Group",
            "cost_centre__directorate__group__group_name": "Name",
        }
        q = MonthlyFigure.pivot.pivot_data(d1.keys())
        self.queryset = q
        self.column_dict = d1
        super().__init__(*args, **kwargs)


class CostClassView(FidoExportMixin, SingleTableView):
    template_name = "forecast/forecast.html"
    sheet_name = "Forecast"
    filterset_class = None
    table_class = ForecastTable
    table_pagination = False

    def get_table_kwargs(self):
        return {"column_dict": self.column_dict}

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it
        # requires the current year, so it is
        # recall each time. Maybe an overkill,
        # but I don't want to risk to forget
        # to change the year!
        columns = {
            "cost_centre__cost_centre_code": "Cost Centre Code",
            "cost_centre__cost_centre_name": "Cost Centre Description",
            "natural_account_code__natural_account_code": "Natural Account Code",
            "natural_account_code__natural_account_code_description": "Natural Account Code Description",  # noqa
            "programme__programme_code": "Programme Code",
            "programme__programme_description": "Programme Description",
            "project_code__project_code": "Project Code",
            "project_code__project_description": "Project Description",
            "programme__budget_type_fk__budget_type_display": "Budget Type",
            "natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping",  # noqa
            "natural_account_code__expenditure_category__grouping_description": "Budget Category",  # noqa
            "natural_account_code__account_L5_code__economic_budget_code": "Expenditure Type",  # noqa
        }
        cost_centre_code = 888812
        pivot_filter = {"cost_centre__cost_centre_code": "{}".format(cost_centre_code)}
        q = MonthlyFigure.pivot.pivot_data(columns.keys(), pivot_filter)
        self.queryset = q
        self.column_dict = columns
        super().__init__(*args, **kwargs)


class MultiForecastView(MultiTableMixin, TemplateView):
    template_name = "forecast/forecastmulti.html"

    # table_pagination = {
    #     'per_page': 30
    # }
    table_pagination = False

    def __init__(self, *args, **kwargs):
        # TODO remove hardcoded cost centre
        # TODO the filter will be set from the request
        cost_centre_code = 888812
        order_list = ["programme__budget_type_fk__budget_type_display_order"]
        pivot_filter = {"cost_centre__cost_centre_code": "{}".format(cost_centre_code)}

        sub_total_type = ["programme__budget_type_fk__budget_type_display"]
        display_sub_total_column = "cost_centre__cost_centre_name"
        q1 = MonthlyFigure.pivot.subtotal_data(
            display_sub_total_column,
            sub_total_type,
            budget_type_columns.keys(),
            pivot_filter,
            order_list=order_list,
        )

        # subtotal_data
        order_list = [
            "programme__budget_type_fk__budget_type_display_order",
            "forecast_expenditure_type__forecast_expenditure_type_display_order",
        ]
        sub_total_prog = [
            "programme__budget_type_fk__budget_type_display",
            "forecast_expenditure_type__forecast_expenditure_type_description",
        ]
        display_sub_total_column = "programme__programme_description"

        q2 = MonthlyFigure.pivot.subtotal_data(
            display_sub_total_column,
            sub_total_prog,
            programme_columns.keys(),
            pivot_filter,
            order_list=order_list,
        )

        sub_total_nac = [
            "programme__budget_type_fk__budget_type_display",
            "natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
        ]
        display_sub_total_column = (
            "natural_account_code__expenditure_category__grouping_description"
        )

        q3 = MonthlyFigure.pivot.subtotal_data(
            display_sub_total_column,
            sub_total_nac,
            natural_account_columns.keys(),
            pivot_filter,
            order_list=order_list,
        )
        self.tables = [
            ForecastSubTotalTable(budget_type_columns, q1),
            ForecastSubTotalTable(programme_columns, q2),
            ForecastSubTotalTable(natural_account_columns, q3),
        ]

        super().__init__(*args, **kwargs)


def pivot_test1(request):
    field_dict = {
        "cost_centre__directorate": "Directorate",
        "cost_centre__directorate__directorate_name": "Name",
        "natural_account_code": "NAC",
    }

    q1 = MonthlyFigure.pivot.pivot_data(
        field_dict.keys(), {"cost_centre__directorate__group": "1090AA"}
    )
    table = ForecastTable(field_dict, q1)
    RequestConfig(request).configure(table)
    return render(request, "forecast/forecast.html", {"table": table})


class AddRowView(FormView):
    template_name = "forecast/add.html"
    form_class = AddForecastRowForm
    financial_year_id = 2019
    cost_centre_code = None

    def get_cost_centre(self):
        if self.cost_centre_code is not None:
            return

        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs["cost_centre_code"]

    def get_success_url(self):
        self.get_cost_centre()

        return reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

    def cost_centre_details(self):
        self.get_cost_centre()

        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.cost_centre_code,
        )
        return {
            "group": cost_centre.directorate.group.group_name,
            "directorate": cost_centre.directorate.directorate_name,
            "cost_centre_name": cost_centre.cost_centre_name,
            "cost_centre_num": cost_centre.cost_centre_code,
        }

    def form_valid(self, form):
        self.get_cost_centre()

        data = form.cleaned_data
        for financial_period in range(1, 13):
            monthly_figure = MonthlyFigure(
                financial_year_id=self.financial_year_id,
                financial_period_id=financial_period,
                cost_centre_id=self.cost_centre_code,
                programme=data["programme"],
                natural_account_code=data["natural_account_code"],
                analysis1_code_id=data["analysis1_code"],
                analysis2_code_id=data["analysis2_code"],
                project_code=data["project_code"],
                amount=0,
            )
            monthly_figure.save()

        return super().form_valid(form)


class EditForecastView(ForecastBaseView):
    template_name = "forecast/edit.html"

    def cost_centre_details(self):
        return {
            "group": "Test group",
            "directorate": "Test directorate",
            "cost_centre_name": "Test cost centre name",
            "cost_centre_num": self.cost_centre_code,
        }

    def table(self):
        field_dict = {
            "cost_centre__directorate": "Directorate",
            "cost_centre__directorate__directorate_name": "Name",
            "natural_account_code": "NAC",
            "cost_centre": self.cost_centre_code,
        }

        q1 = MonthlyFigure.pivot.pivot_data(
            field_dict.keys(), {"cost_centre": self.cost_centre_code}
        )

        return ForecastTable(field_dict, q1)


def edit_forecast_prototype(request):
    financial_year = 2019
    cost_centre_code = "888812"

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            cost_centre_code = form.cleaned_data["cost_centre_code"]
            financial_year = form.cleaned_data["financial_year"]

            cell_data = json.loads(form.cleaned_data["cell_data"])

            for key, cell in cell_data.items():
                if cell["editable"]:
                    monthly_figure = MonthlyFigure.objects.filter(
                        cost_centre__cost_centre_code=cost_centre_code,
                        financial_year__financial_year=financial_year,
                        financial_period__period_short_name__iexact=cell["key"],
                        programme__programme_code=cell["programmeCode"],
                        natural_account_code__natural_account_code=cell[
                            "naturalAccountCode"
                        ],
                    ).first()
                    monthly_figure.amount = int(float(cell["value"]))
                    monthly_figure.save()
    else:
        form = EditForm(
            initial={
                "financial_year": financial_year,
                "cost_centre_code": cost_centre_code,
            }
        )
    pivot_filter = {"cost_centre__cost_centre_code": "{}".format(cost_centre_code)}
    monthly_figures = MonthlyFigure.pivot.pivot_data({}, pivot_filter)

    # TODO - Luisella to restrict to financial year
    editable_periods = list(FinancialPeriod.objects.filter(actual_loaded=False).all())

    editable_periods_dump = serializers.serialize("json", editable_periods)

    forecast_dump = json.dumps(list(monthly_figures), cls=DjangoJSONEncoder)

    return render(
        request,
        "forecast/edit_prototype.html",
        {
            "form": form,
            "editable_periods_dump": editable_periods_dump,
            "forecast_dump": forecast_dump,
        },
    )