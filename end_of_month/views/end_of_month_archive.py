from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic.edit import FormView

from end_of_month.forms import EndOfMonthProcessForm
from end_of_month.utils import user_has_archive_access


class EndOfMonthProcessView(
    UserPassesTestMixin, FormView,
):
    template_name = "end_of_month/end_of_month_archive.html"
    form_class = EndOfMonthProcessForm

    def test_func(self):
        can_edit = user_has_archive_access(
            self.request.user
        )

        if not can_edit:
            raise PermissionDenied()

        return True

    def get_success_url(self):
        """
        TODO add where you want user to go if archiving is successful
        """
        return reverse("index")

    def form_valid(self, form):
        data = form.cleaned_data
        self.period_code = data["period_code"]
        return super(self).form_valid(form)

    def available_for_archiving(self, form, **kwargs):

        context = super().get_context_data(**kwargs)
        context["section_name"] = ""
        context["section_description"] = (
            f"Month to be archived: {self.period_code}"
        )
        return "message about whether you can archive"
