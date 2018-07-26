from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('costcentres/', views.CostcentreListView.as_view(), name='costcentres'),
    path('directorates/', views.DirectorateListView.as_view(), name='directorates'),
    re_path(r'^directorates/(?P<group>\w+)$', views.DirectorateListView.as_view(), name='directorates_by_group'),
    path('groups/', views.DepartmentalGroupListView.as_view(), name='groups'),
    path('groups/', views.DepartmentalGroupListView.as_view(), name='groups1'),
    path('costcentre/', views.costcentre, name='costcentre'),
    path('directorate/', views.directorate, name='directorate'),
    path('departmentalgroup/', views.departmentalgroup, name='departmentalgroup')
]

