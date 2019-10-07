from core.views import FAdminFilteredView

from .filters import Analysis1Filter, Analysis2Filter, CommercialCategoryFilter, ExpenditureCategoryFilter, \
    FCOMappingtFilter, HistoricalAnalysis1Filter, HistoricalAnalysis2Filter, HistoricalCommercialCategoryFilter, \
    HistoricalExpenditureCategoryFilter, HistoricalFCOMappingtFilter, HistoricalInterEntityFilter, HistoricalNACFilter, \
    HistoricalProgrammeFilter, HistoricalProjectFilter, InterEntityFilter, NACFilter, ProgrammeFilter, ProjectFilter
from .tables import Analysis1Table, Analysis2Table, CommercialCategoryTable, ExpenditureCategoryTable, FCOMappingTable, \
    HistoricalAnalysis1Table, HistoricalAnalysis2Table, HistoricalCommercialCategoryTable, \
    HistoricalExpenditureCategoryTable, HistoricalFCOMappingTable, HistoricalInterEntityTable, \
    HistoricalNaturalCodeTable, HistoricalProgrammeTable, HistoricalProjectTable, InterEntityTable, NaturalCodeTable, \
    ProgrammeTable, ProjectTable


class FilteredNACListView(FAdminFilteredView):
    table_class = NaturalCodeTable
    model = table_class.Meta.model
    filterset_class = NACFilter
    name = 'Natural Account Codes (NAC)'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field tells us what we are ' \
                                         'spending the money on. ' \
                                         'The structure follows the Treasury Common Chart of ' \
                                         'Accounts and groups a set of transactions ' \
                                         'into a clearly defined category.'
        return context


class HistoricalFilteredNACListView(FilteredNACListView):
    table_class = HistoricalNaturalCodeTable
    model = table_class.Meta.model
    filterset_class = HistoricalNACFilter
    name = 'Natural Account Codes  2018-19'


class FilteredExpenditureCategoryListView(FAdminFilteredView):
    table_class = ExpenditureCategoryTable
    model = table_class.Meta.model
    filterset_class = ExpenditureCategoryFilter
    name = 'Budget Categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field helps you in acquiring the correct ' \
                                         'Natural Account Code for your purchase ' \
                                         'from a financial perspective.'
        return context


class HistoricalFilteredExpenditureCategoryListView(FilteredExpenditureCategoryListView):
    table_class = HistoricalExpenditureCategoryTable
    model = table_class.Meta.model
    filterset_class = HistoricalExpenditureCategoryFilter
    name = 'Budget Categories 2018-19'


class FilteredCommercialCategoryListView(FAdminFilteredView):
    table_class = CommercialCategoryTable
    model = table_class.Meta.model
    filterset_class = CommercialCategoryFilter
    name = 'Commercial Categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field helps you in acquiring the correct ' \
                                         'Natural Account Code for your purchase ' \
                                         'from a procurement perspective.'
        return context


class HistoricalFilteredCommercialCategoryListView(FilteredCommercialCategoryListView):
    table_class = HistoricalCommercialCategoryTable
    model = table_class.Meta.model
    filterset_class = HistoricalCommercialCategoryFilter
    name = 'Commercial Categories 2018-19'


class FilteredAnalysis1ListView(FAdminFilteredView):
    table_class = Analysis1Table
    model = table_class.Meta.model
    filterset_class = Analysis1Filter
    name = 'Contract Reconciliation (Analysis 1)'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field helps to ' \
                                         'reconcile with Commercial’s unique ' \
                                         'contract identifier. It will enable the organisation ' \
                                         'to match spend on the financial system ' \
                                         'to specific contracts.'
        return context


class HistoricalFilteredAnalysis1ListView(FilteredAnalysis1ListView):
    table_class = HistoricalAnalysis1Table
    model = table_class.Meta.model
    filterset_class = HistoricalAnalysis1Filter
    name = 'Contract Reconciliation (Analysis 1) 2018-19'


class FilteredAnalysis2ListView(FAdminFilteredView):
    table_class = Analysis2Table
    model = table_class.Meta.model
    filterset_class = Analysis2Filter
    name = 'Markets (Analysis 2)'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field is used by the Overseas Team. ' \
                                         'The cost centre structure  identifies our 9 regions, ' \
                                         'however, within each region ' \
                                         'the spend is needed by country.'
        return context


class HistoricalFilteredAnalysis2ListView(FilteredAnalysis2ListView):
    table_class = HistoricalAnalysis2Table
    model = table_class.Meta.model
    filterset_class = HistoricalAnalysis2Filter
    name = 'Markets (Analysis 2) 2018-19'


class FilteredProgrammeView(FAdminFilteredView):
    table_class = ProgrammeTable
    model = table_class.Meta.model
    filterset_class = ProgrammeFilter
    name = 'Programme Codes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field tells us why we are spending the money ' \
                                         'i.e. what we are trying to deliver on. ' \
                                         'This reflects the two most important reporting ' \
                                         'requirements that DIT is likely to have to HMG over ' \
                                         'the next few years (EU exit and ODA) ' \
                                         'and Parliament Control Total ' \
                                         '(DEL/AME and Admin/Programme).'
        return context


class HistoricalFilteredProgrammeView(FilteredProgrammeView):
    table_class = HistoricalProgrammeTable
    model = table_class.Meta.model
    filterset_class = HistoricalProgrammeFilter
    name = 'Programme Codes 2018-19'


class FilteredInterEntityView(FAdminFilteredView):
    table_class = InterEntityTable
    model = table_class.Meta.model
    filterset_class = InterEntityFilter
    name = 'Entity Inter Entity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field is used to identify transactions with ' \
                                         'Other Government Departments (OGDs) / Bodies which ' \
                                         'is needed for the year-end accounts. To be used ' \
                                         'when setting up Purchase Orders and / or ' \
                                         'journals with OGDs.'
        return context


class HistoricalFilteredInterEntityView(FilteredInterEntityView):
    table_class = HistoricalInterEntityTable
    model = table_class.Meta.model
    filterset_class = HistoricalInterEntityFilter
    name = 'Entity Inter Entity 2018-19'


class FilteredProjectView(FAdminFilteredView):
    table_class = ProjectTable
    model = table_class.Meta.model
    filterset_class = ProjectFilter
    name = 'Project Codes (Spare 1)'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = 'This field helps to identify DITs project / portfolio ' \
                                         'and report against them regardless where in the ' \
                                         'organisation expenditure is taking place i.e. ' \
                                         'Trade Remedies Authority (project) ' \
                                         'expenditure in TPG, ' \
                                         'Digital and Estates.'
        return context


class HistoricalFilteredProjectView(FilteredProjectView):
    table_class = HistoricalProjectTable
    model = table_class.Meta.model
    filterset_class = HistoricalProjectFilter
    name = 'Project Codes (Spare 1) 2018-19'


class FilteredFCOMappingView(FAdminFilteredView):
    table_class = FCOMappingTable
    model = table_class.Meta.model
    filterset_class = FCOMappingtFilter
    name = 'FCO Mappings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.name
        context['section_description'] = ''
        return context


class HistoricalFilteredFCOMappingView(FilteredFCOMappingView):
    table_class = HistoricalFCOMappingTable
    model = table_class.Meta.model
    filterset_class = HistoricalFCOMappingtFilter
    name = 'FCO Mappings 2018-19'