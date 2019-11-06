from django.urls import path

from upload_file.views import (
    DocumentsView,
    SuccessfulUploadView,
    UploadedView,
)

urlpatterns = [
    path("success/", SuccessfulUploadView.as_view(), name="upload_success"),
    path("files/", UploadedView.as_view(), name="uploaded_files"),
    path("documents/", DocumentsView.as_view(), name="upload_documents"),
]
