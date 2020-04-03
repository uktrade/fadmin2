from django.urls import path

from core import views
from gifthospitality.views import GiftHospitalityOfferedDoneView

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.AboutView.as_view(), name="about"),
    path("logout", views.logout, name="logout"),
    path("testupload", views.DocumentCreateView.as_view(), name="testupload"),
    path("gifthospitality/offered", GiftHospitalityOfferedDoneView.as_view(), name="offered-done"),
]
