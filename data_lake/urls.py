from django.urls import path

from .views import (
    ForecastViewSet,
    haha
)

urlpatterns = [
    path(
        "haha/",
        haha,
        #ForecastViewSet.as_view({'get': 'list'}),
        name="haha",
    ),
    path(
        "forecast/",
        ForecastViewSet.as_view({'get': 'list'}),
        name="data_lake_forecast",
    ),
]
