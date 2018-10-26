from core.filters import MyFilterSet

import django_filters

from django.db.models import Q

from .models import Analysis1, Analysis2, CommercialCategory, \
    ExpenditureCategory, NaturalCode, ProgrammeCode


class NACFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(account_L5_code__economic_budget_code__icontains=value) |
                               Q(expenditure_category__NAC_category__NAC_category_description__icontains=value) |
                               Q(expenditure_category__linked_budget_code__natural_account_code_description__icontains=value) |
                               Q(expenditure_category__linked_budget_code__natural_account_code__icontains=value) |
                               Q(expenditure_category__grouping_description__icontains=value) |
                               Q(commercial_category__commercial_category__icontains=value) |
                               Q(natural_account_code__icontains=value) |
                               Q(natural_account_code_description__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = NaturalCode
        fields = ['search_all']

    @property
    def qs(self):
        nac = super(NACFilter, self).qs
        return nac.filter(active=True).order_by('-account_L5_code__economic_budget_code',
                                                'commercial_category',
                                                'expenditure_category__NAC_category',
                                                'expenditure_category',
                                                'expenditure_category__linked_budget_code',
                                                'natural_account_code',
                                                'natural_account_code_description')


class ExpenditureCategoryFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                                method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(NAC_category__NAC_category_description__icontains=value) |
                               Q(grouping_description__icontains=value) |
                               Q(description__icontains=value) |
                               Q(further_description__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = ExpenditureCategory
        fields = ['search_all']

    @property
    def qs(self):
        cat_filter = super(ExpenditureCategoryFilter, self).qs
        return cat_filter.order_by('NAC_category',
                                          'grouping_description',
                                          'description',
                                          'further_description')


class CommercialCategoryFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                                method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(commercial_category__icontains=value) |
                               Q(description__icontains=value))

    class Meta(MyFilterSet.Meta):
        model = CommercialCategory
        fields = ['search_all']

    @property
    def qs(self):
        cat_filter = super(CommercialCategoryFilter, self).qs
        return cat_filter.order_by('commercial_category',
                                          'description'
                                          )


class Analysis1Filter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                                method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(analysis1_code__icontains=value) |
                               Q(analysis1_description__icontains=value))

    class Meta(MyFilterSet.Meta):
        model = Analysis1
        fields = ['search_all']

    @property
    def qs(self):
        an1_filter = super(Analysis1Filter, self).qs
        return an1_filter.order_by('analysis1_code',
                                          'analysis1_description'
                                          )


class Analysis2Filter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                                method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(analysis2_code__icontains=value) |
                               Q(analysis2_description__icontains=value))

    class Meta(MyFilterSet.Meta):
        model = Analysis2
        fields = ['search_all']

    @property
    def qs(self):
        an2_filter = super(Analysis2Filter, self).qs
        return an2_filter.order_by('analysis2_code',
                                          'analysis2_description'
                                          )


class ProgrammeFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                                method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(programme_code__icontains=value) |
                               Q(programme_description__icontains=value) |
                               Q(budget_type__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = ProgrammeCode
        fields = [
            'search_all',
        ]

    @property
    def qs(self):
        prog = super(ProgrammeFilter, self).qs
        return prog.filter(active=True).order_by('programme_code',
                                                 'programme_description',
                                                 'budget_type')
