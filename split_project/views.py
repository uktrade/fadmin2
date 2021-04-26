import logging
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.urls import reverse

from forecast.views.upload_file import UploadViewBase

from split_project.forms import UploadPercentageForm

from upload_file.models import FileUpload
from upload_file.utils import user_has_upload_permission


logger = logging.getLogger(__name__)


class UploadPercentageView(UploadViewBase):
    form_class = UploadPercentageForm

    context = "Upload Percentages"
    upload_type = FileUpload.PROJECTPERCENTAGE


    def test_func(self):
        return user_has_upload_permission(self.request.user)



class UploadedPercentageView(UserPassesTestMixin, TemplateView):
    template_name = "split_projects.html"

    def test_func(self):
        return user_has_upload_permission(self.request.user)

    def handle_no_permission(self):
        return redirect(reverse("index",))

    def uploaded_files(self):
        uploaded_files = FileUpload.objects.filter(
            Q(document_type=FileUpload.PROJECTPERCENTAGE)
        ).order_by("-created")

        return uploaded_files


def export_split_percentage_data(request):
    print("Called export split percentage")


def export_split_percentage_template(request):
    print("Called export template")
