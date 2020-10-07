from django.urls import path

from .views import (
    haha
)

urlpatterns = [
    path(
        "forecast/",
        haha,
        #ForecastViewSet.as_view({'get': 'list'}),
        name="data_lake_forecast",
    ),
]
