from django.urls import path

from upload_file.views import (
    UploadFileView,
    SuccessfulUploadView,
)

urlpatterns = [
    path("upload-file/", UploadFileView.as_view(), name="upload_file"),
    path("upload-success/", SuccessfulUploadView.as_view(), name="upload_success"),
]
