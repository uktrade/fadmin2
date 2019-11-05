from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from forecast.forms import (
    UploadFileForm,
)

from upload_file.models import FileUpload
from upload_file.tasks import process_uploaded_file


class SuccessfulUploadView(TemplateView):
    template_name = "core/info.html"

    def heading(self):
        return "Your upload was successful"

    def message(self):
        return "You have successfully " \
               "uploaded a file, it will" \
               " be processed shortly."
