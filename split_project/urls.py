from django.urls import path

from split_project.views import UploadPercentageView

urlpatterns = [
    path(
        "upload_percentage/", UploadPercentageView.as_view(), name="upload_percentage"
    ),
]
