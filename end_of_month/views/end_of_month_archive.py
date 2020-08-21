from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.forms import EndOfMonthProcessForm
from end_of_month.models import EndOfMonthStatus
from end_of_month.utils import user_has_archive_access

from forecast.utils.access_helpers import is_system_locked


class EndOfMonthProcessView(
    UserPassesTestMixin, FormView,
):
    template_name = "end_of_month/end_of_month_archive.html"
    form_class = EndOfMonthProcessForm
    period_code = None
    success_url = reverse_lazy("end_of_month")

    def test_func(self):
        can_edit = user_has_archive_access(
            self.request.user
        )

        if not can_edit:
            raise PermissionDenied()

        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locked"] = is_system_locked()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        end_of_month_status = data["period_code_options"]
        end_of_month_archive(end_of_month_status.archived_period.financial_period_code)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    #
    # def available_for_archiving(self, form, **kwargs):
    #
    #     context = super().get_context_data(**kwargs)
    #     context["section_name"] = ""
    #     context["section_description"] = (
    #         f"Month to be archived: {self.period_code}"
    #     )
    #     return context
    #
    # def forecast_not_locked(self, form, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["section_name"] = "Archiving not available"
    #     context["section_description"] = (
    #         f"Forecast is not locked"
    #     )
    #     return context
    #
    # def archiving_previously_performed(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["section_name"] = "Nothing to archive"
    #     context["section_description"] = (
    #         f"Last archive for {self.period_code} ran on {self.date}"
    #     )
    #     return context
