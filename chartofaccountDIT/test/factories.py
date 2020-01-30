import factory

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    ArchiveAnalysis1,
    ArchiveAnalysis2,
    ArchiveCommercialCategory,
    ArchiveExpenditureCategory,
    ArchiveFCOMapping,
    ArchiveInterEntity,
    ArchiveNaturalCode,
    ArchiveProgrammeCode,
    ArchiveProjectCode,
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


class Analysis1Factory(factory.DjangoModelFactory):
    """
    Define Analysis1 Factory
    """

    class Meta:
        model = Analysis1

    active = True


class HistoricalAnalysis1Factory(factory.DjangoModelFactory):
    """
    Define ArchiveAnalysis1 Factory
    """

    class Meta:
        model = ArchiveAnalysis1


class Analysis2Factory(factory.DjangoModelFactory):
    """
    Define Analysis2 Factory
    """

    class Meta:
        model = Analysis2

    active = True


class HistoricalAnalysis2Factory(factory.DjangoModelFactory):
    """
    Define ArchiveAnalysis2 Factory
    """

    class Meta:
        model = ArchiveAnalysis2


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

    class Meta:
        model = ExpenditureCategory


class HistoricalExpenditureCategoryFactory(factory.DjangoModelFactory):
    """
    Define ArchiveExpenditureCategory Factory
    """

    class Meta:
        model = ArchiveExpenditureCategory


class CommercialCategoryFactory(factory.DjangoModelFactory):
    """
    Define CommercialCategory Factory
    """

    class Meta:
        model = CommercialCategory


class HistoricalCommercialCategoryFactory(factory.DjangoModelFactory):
    """
    Define ArchiveCommercialCategory Factory
    """

    class Meta:
        model = ArchiveCommercialCategory


class NaturalCodeFactory(factory.DjangoModelFactory):
    """
    Define NaturalCode Factory
    """

    class Meta:
        model = NaturalCode

    active = True
    natural_account_code = 999999
    natural_account_code_description = "NAC description"
    used_for_budget = False


class HistoricalNaturalCodeFactory(factory.DjangoModelFactory):
    """
    Define ArchiveNaturalCode Factory
    """

    class Meta:
        model = ArchiveNaturalCode


class ProgrammeCodeFactory(factory.django.DjangoModelFactory):
    """
    Define ProgrammeCode Factory
    """

    class Meta:
        model = ProgrammeCode

    active = True
    programme_code = "123456"
    programme_description = "Programme Test description"
    budget_type_fk = factory.Iterator(BudgetType.objects.all())


class HistoricalProgrammeCodeFactory(factory.DjangoModelFactory):
    """
    Define ArchiveProgrammeCode Factory
    """

    class Meta:
        model = ArchiveProgrammeCode


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
    Define ArchiveInterEntity Factory
    """

    class Meta:
        model = ArchiveInterEntity


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
    Define ArchiveProjectCode Factory
    """

    class Meta:
        model = ArchiveProjectCode


class FCOMappingFactory(factory.DjangoModelFactory):
    """
    Define FCOMapping Factory
    """

    class Meta:
        model = FCOMapping


class HistoricalFCOMappingFactory(factory.DjangoModelFactory):
    """
    Define ArchiveFCOMapping Factory
    """

    class Meta:
        model = ArchiveFCOMapping
