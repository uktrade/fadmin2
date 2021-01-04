import factory

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedCommercialCategory,
    ArchivedExpenditureCategory,
    ArchivedFCOMapping,
    ArchivedInterEntity,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
    BudgetType,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    InterEntityL1,
    NACCategory,
    NaturalCode,
    OperatingDeliveryCategory,
    ProgrammeCode,
    ProjectCode,
)

from core.models import FinancialYear


class Analysis1Factory(factory.DjangoModelFactory):
    """
    Define Analysis1 Factory
    """

    class Meta:
        model = Analysis1

    active = True


class HistoricalAnalysis1Factory(factory.DjangoModelFactory):
    """
    Define ArchivedAnalysis1 Factory
    """
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedAnalysis1


class Analysis2Factory(factory.DjangoModelFactory):
    """
    Define Analysis2 Factory
    """

    class Meta:
        model = Analysis2

    active = True


class HistoricalAnalysis2Factory(factory.DjangoModelFactory):
    """
    Define ArchivedAnalysis2 Factory
    """
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedAnalysis2


class NACCategoryFactory(factory.DjangoModelFactory):
    """
    Define NACCategory Factory
    """

    class Meta:
        model = NACCategory

    NAC_category_description = "Test NAC desc"


class OperatingDeliveryCategoryFactory(factory.DjangoModelFactory):
    """
    Define OperatingDeliveryCategory Factory
    """

    class Meta:
        model = OperatingDeliveryCategory


class ExpenditureCategoryFactory(factory.DjangoModelFactory):
    """
    Define ExpenditureCategory Factory
    """

    grouping_description = 'Test Budget Category'
    NAC_category = factory.SubFactory(NACCategoryFactory)

    class Meta:
        model = ExpenditureCategory


class HistoricalExpenditureCategoryFactory(factory.DjangoModelFactory):
    """
    Define ArchivedExpenditureCategory Factory
    """
    grouping_description = 'Test Budget Category'
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedExpenditureCategory


class CommercialCategoryFactory(factory.DjangoModelFactory):
    """
    Define CommercialCategory Factory
    """

    class Meta:
        model = CommercialCategory


class HistoricalCommercialCategoryFactory(factory.DjangoModelFactory):
    """
    Define ArchivedCommercialCategory Factory
    """
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedCommercialCategory


class NaturalCodeFactory(factory.DjangoModelFactory):
    """
    Define NaturalCode Factory
    """

    class Meta:
        model = NaturalCode
        django_get_or_create = ('natural_account_code',)

    active = True
    natural_account_code = 12345678
    natural_account_code_description = "NAC description"
    used_for_budget = False


class HistoricalNaturalCodeFactory(factory.DjangoModelFactory):

    active = True
    natural_account_code = 87654321
    natural_account_code_description = "Historical NAC description"
    used_for_budget = False
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedNaturalCode
        django_get_or_create = (
            "natural_account_code",
            "financial_year",
        )


class ProgrammeCodeFactory(factory.DjangoModelFactory):
    """
    Define ProgrammeCode Factory
    """

    class Meta:
        model = ProgrammeCode
        django_get_or_create = ('programme_code',)

    active = True
    programme_code = "123456"
    programme_description = "Programme Test description"
    budget_type = factory.Iterator(BudgetType.objects.all())


class HistoricalProgrammeCodeFactory(factory.DjangoModelFactory):
    """
    Define ArchivedProgrammeCode Factory
    """
    active = True
    programme_code = "654321"
    programme_description = "Programme Test description"
    budget_type = factory.Iterator(BudgetType.objects.all())
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedProgrammeCode
        django_get_or_create = ('programme_code',
                                'financial_year')


class InterEntityL1Factory(factory.DjangoModelFactory):
    """
    Define InterEntityL1 Factory
    """

    class Meta:
        model = InterEntityL1


class InterEntityFactory(factory.DjangoModelFactory):
    """
    Define InterEntity Factory
    """

    class Meta:
        model = InterEntity


class HistoricalInterEntityFactory(factory.DjangoModelFactory):
    """
    Define ArchivedInterEntity Factory
    """
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedInterEntity


class ProjectCodeFactory(factory.DjangoModelFactory):
    """
    Define ProjectCode Factory
    """

    class Meta:
        model = ProjectCode

    active = True
    project_code = "5000"
    project_description = "Project Description"


class HistoricalProjectCodeFactory(factory.DjangoModelFactory):
    """
    Define ArchivedProjectCode Factory
    """
    active = True
    project_code = "5000"
    project_description = "Project Description"
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedProjectCode


class FCOMappingFactory(factory.DjangoModelFactory):
    """
    Define FCOMapping Factory
    """

    class Meta:
        model = FCOMapping


class HistoricalFCOMappingFactory(factory.DjangoModelFactory):
    """
    Define ArchivedFCOMapping Factory
    """
    financial_year = FinancialYear.objects.get(pk=2019)

    class Meta:
        model = ArchivedFCOMapping
