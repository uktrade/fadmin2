from django.urls import path

from forecast.views.cost_centre_views import (
    ChooseCostCentreView,
)
from forecast.views.forecast_views import (
    AddRowView,
    CostClassView,
    EditForecastView,
    MultiForecastView,
    PivotClassView,
    UploadActualsView,
    edit_forecast_prototype,
    pivot_test1,
)

urlpatterns = [
    path("pivot/", PivotClassView.as_view(), name="pivot"),
    path("costcentre/", CostClassView.as_view(), name="costcentre"),
    path("pivotmulti/", MultiForecastView.as_view(), name="pivotmulti"),
    path("pivot1/", pivot_test1, name="pivot1"),
    path(
        "edit/<int:cost_centre_code>/",
        EditForecastView.as_view(), name="edit_forecast"),
    path(
        "add/<int:cost_centre_code>/",
        AddRowView.as_view(),
        name="add_forecast_row",
    ),
    path(
        "edit-prototype/",
        edit_forecast_prototype,
        name="edit_prototype",
    ),
    path(
        "choose-cost-centre/",
        ChooseCostCentreView.as_view(),
        name="choose_cost_centre",
    ),
    path(
        "upload-file/",
        UploadActualsView.as_view(),
        name="upload_file"
    ),
]
