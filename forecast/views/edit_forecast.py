import json
import re

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from core.models import FinancialYear
from core.myutils import get_current_financial_year

from costcentre.forms import (
    MyCostCentresForm,
)
from costcentre.models import CostCentre

from forecast.forms import (
    AddForecastRowForm,
    EditForecastFigureForm,
    PasteForecastForm,
    PublishForm,
)
from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.permission_shortcuts import (
    NoForecastViewPermission,
    get_objects_for_user,
)
from forecast.serialisers import FinancialCodeSerializer
from forecast.utils.edit_helpers import (
    BadFormatException,
    CannotFindMonthlyFigureException,
    NoFinancialCodeForEditedValue,
    NotEnoughMatchException,
    RowMatchException,
    TooManyMatchException,
    check_cols_match,
    check_row_match,
    get_monthly_figures,
)
from forecast.views.base import (
    CostCentrePermissionTest,
    NoCostCentreCodeInURLError,
)


class ChooseCostCentreView(UserPassesTestMixin, FormView):
    template_name = "forecast/edit/choose_cost_centre.html"
    form_class = MyCostCentresForm
    cost_centre = None

    def test_func(self):
        try:
            cost_centres = get_objects_for_user(
                self.request.user,
                "costcentre.change_costcentre",
            )
        except NoForecastViewPermission:
            raise PermissionDenied()

        # If user has permission on
        # one or more CCs then let them view
        return cost_centres.count() > 0

    def get_form_kwargs(self):
        kwargs = super(ChooseCostCentreView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.cost_centre = form.cleaned_data['cost_centre']
        return super(ChooseCostCentreView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre.cost_centre_code
            }
        )


class AddRowView(CostCentrePermissionTest, FormView):
    template_name = "forecast/edit/add.html"
    form_class = AddForecastRowForm
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
            "cost_centre_code": cost_centre.cost_centre_code,
        }

    def form_valid(self, form):
        self.get_cost_centre()
        data = form.cleaned_data

        financial_code = FinancialCode.objects.filter(
            cost_centre_id=self.cost_centre_code,
            programme=data["programme"],
            natural_account_code=data["natural_account_code"],
            analysis1_code=data["analysis1_code"],
            analysis2_code=data["analysis2_code"],
            project_code=data["project_code"],
        ).first()

        if not financial_code:
            financial_code = FinancialCode.objects.create(
                cost_centre_id=self.cost_centre_code,
                programme=data["programme"],
                natural_account_code=data["natural_account_code"],
                analysis1_code=data["analysis1_code"],
                analysis2_code=data["analysis2_code"],
                project_code=data["project_code"],
            )

        # Create "actual" monthly figures for past months
        actual_months = FinancialPeriod.financial_period_info.actual_period_code_list()

        if len(actual_months) > 0:
            financial_year = get_current_financial_year()

            for actual_month in actual_months:
                ForecastMonthlyFigure.objects.create(
                    financial_code=financial_code,
                    financial_year_id=financial_year,
                    financial_period_id=actual_month,
                )

        return super().form_valid(form)


@require_http_methods(["POST", ])  # noqa: C901
def pasted_forecast_content(request, cost_centre_code):
    # Check user has permission to edit forecast
    if not request.user.has_perm("forecast.can_view_forecasts"):
        raise PermissionDenied()

    # Check that user has permission to edit cost centre
    cost_centre = CostCentre.objects.filter(
        cost_centre_code=cost_centre_code,
    ).first()

    if not (
        request.user.has_perm("view_costcentre", cost_centre) and
        request.user.has_perm("change_costcentre", cost_centre)
    ):
        raise PermissionDenied()

    form = PasteForecastForm(
        request.POST,
    )
    if form.is_valid():
        paste_content = form.cleaned_data['paste_content']
        pasted_at_row = form.cleaned_data.get('pasted_at_row', None)
        all_selected = form.cleaned_data.get('all_selected', False)

        figure_count = ForecastMonthlyFigure.objects.filter(
            financial_code__cost_centre_id=cost_centre_code,
        ).count()

        row_count = figure_count / 12

        rows = paste_content.splitlines()

        if len(rows) == 0:
            return JsonResponse({
                'error': 'Your pasted data is not formatted correctly.'
            },
                status=400,
            )

        if all_selected and row_count < len(rows):
            return JsonResponse({
                'error': (
                    'You have selected all forecast rows '
                    'but the pasted data has too many rows.'
                )
            },
                status=400,
            )

        if all_selected and row_count > len(rows):
            return JsonResponse({
                'error': (
                    'You have selected all forecast rows '
                    'but the pasted data has too few rows.'
                )
            },
                status=400,
            )

        # Check for header row
        start_row = 0
        if rows[0] == "Natural Account Code":
            start_row = 1

        try:
            for index, row in enumerate(rows, start=start_row):
                cell_data = re.split(r'\t', row.rstrip('\t'))

                # Check that pasted at content and desired first row match
                check_row_match(
                    index,
                    pasted_at_row,
                    cell_data,
                )

                # Check cell data length against expected number of cols
                check_cols_match(cell_data)

                get_monthly_figures(
                    cost_centre_code,
                    cell_data,
                )
        except (
                BadFormatException,
                TooManyMatchException,
                NotEnoughMatchException,
                RowMatchException,
                CannotFindMonthlyFigureException,
        ) as ex:
            return JsonResponse({
                'error': str(ex)
            },
                status=400,
            )

        financial_codes = FinancialCode.objects.filter(
            cost_centre_id=cost_centre_code,
        ).prefetch_related(
            'forecast_forecastmonthlyfigures',
            'forecast_forecastmonthlyfigures__financial_period'
        )

        financial_code_serialiser = FinancialCodeSerializer(
            financial_codes,
            many=True,
        )

        return JsonResponse(financial_code_serialiser.data, safe=False)
    else:
        return JsonResponse({
            'error': 'There was a problem with your '
                     'submission, please contact support'
        },
            status=400,
        )


@require_http_methods(["POST", ])
def update_forecast_figure(request, cost_centre_code):
    # Check user has permission to edit forecast
    if not request.user.has_perm("forecast.can_view_forecasts"):
        raise PermissionDenied()

    # Check that user has permission to edit cost centre
    cost_centre = CostCentre.objects.filter(
        cost_centre_code=cost_centre_code,
    ).first()

    if not (
        request.user.has_perm("view_costcentre", cost_centre) and
        request.user.has_perm("change_costcentre", cost_centre)
    ):
        raise PermissionDenied()

    form = EditForecastFigureForm(
        request.POST,
    )

    if form.is_valid():
        financial_year = FinancialYear.objects.filter(current=True).first()

        financial_code = FinancialCode.objects.filter(
            cost_centre=cost_centre,
            natural_account_code=form.cleaned_data['natural_account_code'],
            programme__programme_code=form.cleaned_data['programme_code'],
            analysis1_code__analysis1_code=form.cleaned_data.get(
                'analysis1_code',
                None,
            ),
            analysis2_code__analysis2_code=form.cleaned_data.get(
                'analysis2_code',
                None,
            ),
            project_code__project_code=form.cleaned_data.get(
                'project_code',
                None,
            ),
        )

        month = form.cleaned_data['month']

        if not financial_code.first():
            raise NoFinancialCodeForEditedValue()

        monthly_figure = ForecastMonthlyFigure.objects.filter(
            financial_year=financial_year,
            financial_code=financial_code.first(),
            financial_period__financial_period_code=month,
        ).first()

        if monthly_figure:
            monthly_figure.amount = form.cleaned_data['amount']
        else:
            financial_period = FinancialPeriod.objects.filter(
                financial_period_code=month
            ).first()
            monthly_figure = ForecastMonthlyFigure(
                financial_year=financial_year,
                financial_code=financial_code.first(),
                financial_period=financial_period,
                amount=form.cleaned_data['amount'],
            )

        monthly_figure.save()

        financial_codes = FinancialCode.objects.filter(
            cost_centre_id=cost_centre_code,
        ).prefetch_related(
            'forecast_forecastmonthlyfigures',
            'forecast_forecastmonthlyfigures__financial_period'
        )

        financial_code_serialiser = FinancialCodeSerializer(
            financial_codes,
            many=True,
        )

        return JsonResponse(financial_code_serialiser.data, safe=False)
    else:
        return JsonResponse({
            'error': 'There was a problem with your '
                     'submission, please contact support'
        },
            status=400,
        )


class EditForecastView(
    CostCentrePermissionTest,
    TemplateView,
):
    template_name = "forecast/edit/edit.html"

    def class_name(self):
        return "wide-table"

    def cost_centre_details(self):
        return {
            "group": "Test group",
            "directorate": "Test directorate",
            "cost_centre_name": "Test cost centre name",
            "cost_centre_code": self.cost_centre_code,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = PublishForm(
            initial={
                "cost_centre_code": self.cost_centre_code,
            }
        )

        financial_code = FinancialCode.objects.filter(
            cost_centre_id=self.cost_centre_code,
        ).prefetch_related(
            'forecast_forecastmonthlyfigures',
            'forecast_forecastmonthlyfigures__financial_period'
        )

        financial_code_serialiser = FinancialCodeSerializer(
            financial_code,
            many=True,
        )

        forecast_dump = json.dumps(financial_code_serialiser.data)
        paste_form = PasteForecastForm()

        context["form"] = form
        context["paste_form"] = paste_form
        context["forecast_dump"] = forecast_dump

        return context
