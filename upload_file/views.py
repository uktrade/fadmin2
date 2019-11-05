from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from forecast.forms import (
    UploadFileForm,
)

from upload_file.models import FileUpload
from upload_file.tasks import process_uploaded_file


class UploadFileView(FormView):
    template_name = "forecast/file_upload.html"
    form_class = UploadFileForm
    success_url = reverse_lazy("upload_success")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            file_upload = FileUpload(
                document_file=request.FILES['file']
            )
            file_upload.save()
            # Process file async
            process_uploaded_file.delay()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SuccessfulUploadView(TemplateView):
    template_name = "core/info.html"

    def heading(self):
        return "Your upload was successful"

    def message(self):
        return "You have successfully " \
               "uploaded a file, it will" \
               " be processed shortly."
