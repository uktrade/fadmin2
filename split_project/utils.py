from django.db.models import Sum

from split_project.models import UploadProjectSplitCoefficient


def validate():
    # Reservation.objects.values('day').annotate(cnt=Count('id')).filter(cnt__lte=5)
    too_large = (
        UploadProjectSplitCoefficient.objects.values(
            "financial_period", "financial_code_from"
        )
        .annotate(total="split_coefficient")
        .filter(total__gt=5)
    )
    pass
