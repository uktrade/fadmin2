from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from upload_file.models import FileUpload


class UploadedView(TemplateView):
    template_name = "upload_file/uploaded_files.html"

    def uploaded_files(self):
        uploaded_files = FileUpload.objects.all().order_by(
            "-created"
        )

        return uploaded_files


class SuccessfulUploadView(TemplateView):
    template_name = "core/info.html"

    def heading(self):
        return "Your upload was successful"

    def message(self):
        return "You have successfully " \
               "uploaded a file, it will" \
               " be processed shortly."
