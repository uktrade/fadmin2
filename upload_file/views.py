from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from upload_file.models import FileUpload

from upload_file.decorators import has_actuals_upload_permission


class UploadedView(TemplateView):
    template_name = "upload_file/uploaded_files.html"

    @has_actuals_upload_permission
    def dispatch(self, request, *args, **kwargs):
        return super(UploadedView, self).dispatch(request, *args, **kwargs)

    def uploaded_files(self):
        uploaded_files = FileUpload.objects.all().order_by(
            "-created"
        )

        return uploaded_files
