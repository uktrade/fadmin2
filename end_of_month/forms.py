from django import forms

class EndOfMonthProcessForm(forms.Form):
    period_code = forms.CharField(
        required=True,
    )
    def clean_period_code(self):
        period_code = self.cleaned_data['period_code']
        try:
            validate_period_code(period_code)
        except InvalidPeriodError:
            raise ValidationError("Valid Period is between 1 and 15.")
        except SelectPeriodAlreadyArchivedError:
            raise ValidationError("The selected period has already been archived.")
        except LaterPeriodAlreadyArchivedError:
            raise ValidationError("A later period has already been archived.")
        return period_code