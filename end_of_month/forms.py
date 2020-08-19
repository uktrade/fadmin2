from django import forms

from end_of_month.utils import (
    InvalidPeriodError, LaterPeriodAlreadyArchivedError,
    SelectPeriodAlreadyArchivedError, validate_period_code)

from end_of_month.models import EndOfMonthStatus


class EndOfMonthProcessForm(forms.Form):
    period_code = forms.CharField(
        required=True,
    )
    date = EndOfMonthStatus.archived_date

    def clean_period_code(self):
        period_code = self.cleaned_data['period_code']
        try:
            validate_period_code(period_code)
        except InvalidPeriodError:
            raise forms.ValidationError("Valid Period is between 1 and 15.")
        except SelectPeriodAlreadyArchivedError:
            raise forms.ValidationError("The selected period has already "
                                        "been archived.")
        except LaterPeriodAlreadyArchivedError:
            raise forms.ValidationError("A later period has already been archived.")
        return period_code
