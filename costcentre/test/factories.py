import factory

from faker import Faker

from costcentre.models import (
    ArchivedCostCentre,
    CostCentre,
    DepartmentalGroup,
    Directorate,
)

fake = Faker()


class DepartmentalGroupFactory(factory.DjangoModelFactory):
    """
        Define DepartmentalGroup Factory
    """

    class Meta:
        model = DepartmentalGroup
        django_get_or_create = ('group_code',)

    group_name = fake.company()
    group_code = str(fake.pyint())
    active = True


class DirectorateFactory(factory.DjangoModelFactory):

    class Meta:
        model = Directorate
        django_get_or_create = ('directorate_code',)

    directorate_name = fake.company()
    directorate_code = str(fake.pyint())
    group = factory.SubFactory(DepartmentalGroupFactory)
    active = True


class CostCentreFactory(factory.DjangoModelFactory):
    """
        Define CostCentre Factory
    """

    class Meta:
        model = CostCentre
        django_get_or_create = ('cost_centre_code',)

    active = True
    directorate = factory.SubFactory(DirectorateFactory)
    cost_centre_code = 999999
    cost_centre_name = "Test Cost Centre"


class ArchivedCostCentreFactory(factory.DjangoModelFactory):

    class Meta:
        model = ArchivedCostCentre
        django_get_or_create = ('cost_centre_code',
                                'financial_year',)

    active = True
    cost_centre_code = 999999
    cost_centre_name = "Test Cost Centre"
    financial_year = 2019
