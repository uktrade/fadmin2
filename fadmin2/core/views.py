from django.shortcuts import render


from django_tables2.export.views import ExportMixin

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render (
        request, 'core/index.html'
     )


class FAdminFilteredView(ExportMixin, SingleTableMixin, FilterView):
    paginate_by = 50
    template_name = 'core/table_filter_generic.html'
    strict = False
