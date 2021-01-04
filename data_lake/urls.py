from django.urls import path

from data_lake.views.forecast import ForecastViewSet

from data_lake.views.cost_centre_hierarchy import HierarchyViewSet
from data_lake.views.natural_code import NaturalCodeViewSet

urlpatterns = [
    path(
        "forecast/",
        ForecastViewSet.as_view({"get": "list"}),
        name="data_lake_forecast",
    ),
    path(
        "hierarchy/",
        HierarchyViewSet.as_view({"get": "list"}),
        name="data_lake_hierachy",
    ),
    path(
        "naturalcode/",
        NaturalCodeViewSet.as_view({"get": "list"}),
        name="data_lake_natural_code",
    ),
]
