from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from upload_file.models import FileUpload


class UploadedView(TemplateView):
    template_name = "upload_file/uploaded_files.html"

    def uploaded_files(self):
        uploaded_files = FileUpload.objects.all().order_by(
            "-created"
        )
        paginator = Paginator(uploaded_files, 5)

        page = self.request.GET.get('page')

        return paginator.get_page(page)


class SuccessfulUploadView(TemplateView):
    template_name = "core/info.html"

    def heading(self):
        return "Your upload was successful"

    def message(self):
        return "You have successfully " \
               "uploaded a file, it will" \
               " be processed shortly."
