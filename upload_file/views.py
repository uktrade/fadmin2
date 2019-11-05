from django.views.generic.base import TemplateView


class SuccessfulUploadView(TemplateView):
    template_name = "core/info.html"

    def heading(self):
        return "Your upload was successful"

    def message(self):
        return "You have successfully " \
               "uploaded a file, it will" \
               " be processed shortly."
