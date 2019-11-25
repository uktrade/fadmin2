import json
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from core.utils import check_empty

from costcentre.forms import (
    MyCostCentresForm,
)
from costcentre.models import CostCentre

from forecast.forms import (
    AddForecastRowForm,
    EditForm,
    PasteForecastForm,
    UploadActualsForm,
)
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)
from forecast.permission_shortcuts import (
    NoForecastViewPermission,
    get_objects_for_user,
)
from forecast.tables import (
    ForecastTable,
)
from forecast.tasks import process_uploaded_file
from forecast.views.base import (
    CostCentrePermissionTest,
    NoCostCentreCodeInURLError,
)

from upload_file.decorators import has_upload_permission
from upload_file.models import FileUpload

TEST_COST_CENTRE = 888812
TEST_FINANCIAL_YEAR = 2019


class MismatchedRowException(Exception):
    pass


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
    financial_year_id = TEST_FINANCIAL_YEAR
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

        # Don't add months that are actuals
        for financial_period in range(1, 13):
            monthly_figure = MonthlyFigure(
                financial_year_id=self.financial_year_id,
                financial_period_id=financial_period,
                cost_centre_id=self.cost_centre_code,
                programme=data["programme"],
                natural_account_code=data["natural_account_code"],
                analysis1_code=data["analysis1_code"],
                analysis2_code=data["analysis2_code"],
                project_code=data["project_code"],
                amount=0,
            )
            monthly_figure.save()

        return super().form_valid(form)


class UploadActualsView(FormView):
    template_name = "forecast/file_upload.html"
    form_class = UploadActualsForm
    success_url = reverse_lazy("uploaded_files")

    @has_upload_permission
    def dispatch(self, *args, **kwargs):
        return super(UploadActualsView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            data = form.cleaned_data

            file_upload = FileUpload(
                document_file=request.FILES['file'],
                uploading_user=request.user,
            )
            file_upload.save()
            # Process file async

            if settings.ASYNC_FILE_UPLOAD:
                process_uploaded_file.delay(
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )
            else:
                process_uploaded_file(
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# TODO permission decorator
@require_http_methods(["POST", ])
def pasted_forecast_content(request, cost_centre_code):
    form = PasteForecastForm(
        request.POST,
    )
    if form.is_valid():
        # TODO check user has permission on cost centre

        paste_content = form.cleaned_data['paste_content']
        pasted_at_row = None
        all_selected = False

        if form.cleaned_data['pasted_at_row']:
            pasted_at_row = json.loads(form.cleaned_data['pasted_at_row'])

        if form.cleaned_data['all_selected']:
            all_selected = form.cleaned_data['all_selected']

        rows = paste_content.splitlines()

        pivot_filter = {"cost_centre__cost_centre_code": "{}".format(
            cost_centre_code
        )}
        output = MonthlyFigure.pivot.pivot_data({}, pivot_filter)
        forecast_dump = list(output)

        test = len(forecast_dump)
        test1 = len(rows)

        if all_selected and len(forecast_dump) != len(rows):
            return JsonResponse({
                'error': 'Your pasted data does not match the selected rows.'
            },
                status=400,
            )

        actuals_count = FinancialPeriod.objects.filter(
            actual_loaded=True
        ).count()
        start_period = 1 + actuals_count

        monthly_figures = []

        # Check for header row
        start_row = 0
        if rows[0] == "Natural Account Code":
            start_row = 1

        num_meta_cols = 5

        for index, row in enumerate(rows, start=start_row):
            cell_data = re.split(r'\t', row.rstrip('\t'))

            if index == 0:
                # Check that pasted at content and desired first row match
                if pasted_at_row:
                    if (
                        pasted_at_row["natural_account_code__natural_account_code"] != cell_data[0] or
                        pasted_at_row["programme__programme_code"] != cell_data[1] or
                        pasted_at_row["analysis1_code__analysis1_code"] != check_empty(cell_data[2]) or
                        pasted_at_row["analysis2_code__analysis2_code"] != check_empty(cell_data[3]) or
                        pasted_at_row["project_code__project_code"] != check_empty(cell_data[4])
                    ):
                        return JsonResponse({
                            'error': 'Your pasted data does not match your selected row.'
                            },
                            status=400,
                        )

            # Check cell data length against expected number of cols
            if len(cell_data) != 12 + num_meta_cols:
                return JsonResponse({
                    'error': 'Your pasted data does not '
                             'match the expected format. '
                             'There are not enough columns.'
                    },
                    status=400,
                )
            else:
                for financial_period in range(start_period, 13):
                    monthly_figure = MonthlyFigure.objects.filter(
                        cost_centre__cost_centre_code=cost_centre_code,
                        financial_year__financial_year=TEST_FINANCIAL_YEAR,
                        financial_period__financial_period_code=financial_period,
                        programme__programme_code=check_empty(cell_data[1]),
                        natural_account_code__natural_account_code=cell_data[0],
                        analysis1_code=check_empty(cell_data[2]),
                        analysis2_code=check_empty(cell_data[3]),
                        project_code=check_empty(cell_data[4]),
                    ).first()

                    if not monthly_figure:
                        return JsonResponse({
                            'error': 'Cannot find matching row for one of your inputs, '
                                     'please check your source material'
                        },
                            status=400,
                        )

                    new_value = int(cell_data[(num_meta_cols + financial_period) - 1])
                    monthly_figure.amount = new_value  # * 100

                    # Don't save yet in case there is an error
                    monthly_figures.append(monthly_figure)

        # Update monthly figures
        for monthly_figure in monthly_figures:
            monthly_figure.save()

        pivot_filter = {"cost_centre__cost_centre_code": "{}".format(
            cost_centre_code
        )}
        output = MonthlyFigure.pivot.pivot_data({}, pivot_filter)
        forecast_dump = list(output)

        return JsonResponse(forecast_dump, safe=False)
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
    financial_year = TEST_FINANCIAL_YEAR

    def cost_centre_details(self):
        return {
            "group": "Test group",
            "directorate": "Test directorate",
            "cost_centre_name": "Test cost centre name",
            "cost_centre_num": self.cost_centre_code,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = EditForm(
            initial={
                "financial_year": self.financial_year,
                "cost_centre_code": self.cost_centre_code,
            }
        )

        pivot_filter = {"cost_centre__cost_centre_code": "{}".format(
            self.cost_centre_code
        )}
        monthly_figures = MonthlyFigure.pivot.pivot_data({}, pivot_filter)

        # TODO - Luisella to restrict to financial year
        actuals_periods = list(FinancialPeriod.objects.filter(actual_loaded=True).all())
        actuals_periods_dump = serializers.serialize("json", actuals_periods)
        forecast_dump = json.dumps(list(monthly_figures), cls=DjangoJSONEncoder)
        paste_form = PasteForecastForm()

        context["form"] = form
        context["paste_form"] = paste_form
        context["actuals_periods_dump"] = actuals_periods_dump
        context["forecast_dump"] = forecast_dump
        return context

    def post(self):
        form = EditForm(self.request.POST)
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
