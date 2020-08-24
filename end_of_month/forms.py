from django import forms
from django.forms import Select

from end_of_month.models import EndOfMonthStatus
from end_of_month.utils import (
    InvalidPeriodError,
    LaterPeriodAlreadyArchivedError,
    SelectPeriodAlreadyArchivedError,
    validate_period_code,
    get_archivable_month,
)


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return f"{obj.archived_period.financial_period_code} - {obj.archived_period.period_long_name}"


class EndOfMonthProcessForm(forms.Form):
    archive_confirmation = forms.BooleanField(required=True, label="Please confirm you would like to archive this month")
    # TODO - Create checkbox template and update class
    archive_confirmation.widget.attrs.update(
        {"class": "govuk-checkboxes__item"}
    )

    def clean_archive_confirmation(self):
        try:
            is_confirmed = self.cleaned_data['archive_confirmation']
            if not is_confirmed:
                raise forms.ValidationError("You must confirm you wish to archive in order to proceed")
            archivable_period = get_archivable_month()

            validate_period_code(archivable_period)
        except InvalidPeriodError:
            raise forms.ValidationError("Valid Period is between 1 and 15.")
        except SelectPeriodAlreadyArchivedError:
            raise forms.ValidationError("The selected period has already "
                                        "been archived.")
        except LaterPeriodAlreadyArchivedError:
            raise forms.ValidationError("A later period has already been archived.")
        return is_confirmed
