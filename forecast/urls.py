from django.urls import path

from forecast.views import (
    AddRowView,
    CostClassView,
    EditForecastView,
    MultiForecastView,
    PivotClassView,
    UploadFileView,
    SuccessfulUploadView,
    edit_forecast_prototype,
    pivot_test1,
)

urlpatterns = [
    path("pivot/", PivotClassView.as_view(), name="pivot"),
    path("costcentre/", CostClassView.as_view(), name="costcentre"),
    path("pivotmulti/", MultiForecastView.as_view(), name="pivotmulti"),
    path("pivot1/", pivot_test1, name="pivot1"),
    path("edit/", EditForecastView.as_view(), name="edit_forecast"),
    path("add/", AddRowView.as_view(), name="add_forecast_row"),
    path("edit-prototype/", edit_forecast_prototype, name="edit_prototype"),
    path("upload-file/", UploadFileView.as_view(), name="upload_file"),
    path("upload-success/", SuccessfulUploadView.as_view(), name="upload_success"),
]
