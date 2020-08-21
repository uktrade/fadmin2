from django import forms
from django.forms import Select

from end_of_month.models import EndOfMonthStatus
from end_of_month.utils import (
    InvalidPeriodError, LaterPeriodAlreadyArchivedError,
    SelectPeriodAlreadyArchivedError, validate_period_code)


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return f"{obj.archived_period.financial_period_code} - {obj.archived_period.period_long_name}"


class EndOfMonthProcessForm(forms.Form):
    period_code_options = UserModelChoiceField(
        queryset=EndOfMonthStatus.objects.filter(
            archived=False,
        ),
        widget=Select(),
    )
    period_code_options.widget.attrs.update(
        {
            "class": "govuk-select",
        }
    )

    def clean_archive_confirmation(self):
        try:
            is_confirmed = self.cleaned_data['archive_confirmation']
            if not is_confirmed:
                raise forms.ValidationError("You must confirm you wish to archive in order to proceed")
                period_code = self.render_to_response(self.get_context_data(form=form))
            validate_period_code(period_code)
        except InvalidPeriodError:
            raise forms.ValidationError("Valid Period is between 1 and 15.")
        except SelectPeriodAlreadyArchivedError:
            raise forms.ValidationError("The selected period has already "
                                        "been archived.")
        except LaterPeriodAlreadyArchivedError:
            raise forms.ValidationError("A later period has already been archived.")
        return is_confirmed
