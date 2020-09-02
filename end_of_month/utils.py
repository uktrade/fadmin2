from end_of_month.models import (
    EndOfMonthStatus)

from forecast.models import FinancialPeriod


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
    period_code = int(period_code)
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


def get_archivable_month():
    first_month_without_actual = FinancialPeriod.financial_period_info.actual_month() + 1
    if first_month_without_actual > FinancialPeriod.financial_period_info.get_max_period().financial_period_code:
        raise InvalidPeriodError()
    is_archived = EndOfMonthStatus.objects.filter(
        archived=True, archived_period__financial_period_code=first_month_without_actual
    ).first()
    if is_archived:
        financial_period = FinancialPeriod.objects.get(financial_period_code=first_month_without_actual)
        raise SelectPeriodAlreadyArchivedError(f"Period {financial_period.period_long_name} already archived")

    return first_month_without_actual
