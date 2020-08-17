from end_of_month.models import (
    EndOfMonthStatus)


class InvalidPeriodError(Exception):
    pass


class SelectPeriodAlreadyArchivedError(Exception):
    pass


class LaterPeriodAlreadyArchivedError(Exception):
    pass


def user_has_archive_access(user):
    if user.groups.filter(name="Finance Administrator") or user.is_superuser:
        return True


def validate_period_code(period_code, **options):
    period_code = options["period"]
    if period_code > 15 or period_code < 1:
        raise InvalidPeriodError()
    end_of_month_info = EndOfMonthStatus.objects.filter(
        archived_period__financial_period_code=period_code
    ).first()
    if end_of_month_info.archived:
        raise SelectPeriodAlreadyArchivedError()
    highest_archived = EndOfMonthStatus.objects.filter(
        archived=True, archived_period__financial_period_code=period_code
    )
    if highest_archived.count():
        raise LaterPeriodAlreadyArchivedError()
