from django.urls import path

from upload_file.views import (
    SuccessfulUploadView,
    UploadedView,
)

urlpatterns = [
    path("success/", SuccessfulUploadView.as_view(), name="upload_success"),
    path("files/", UploadedView.as_view(), name="uploaded_files"),
]
