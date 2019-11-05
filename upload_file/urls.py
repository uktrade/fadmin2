from django.urls import path

from upload_file.views import (
    SuccessfulUploadView,
)

urlpatterns = [
    path("upload-success/", SuccessfulUploadView.as_view(), name="upload_success"),
]
