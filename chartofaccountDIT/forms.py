
from django import forms
from django.forms import Select

from chartofaccountDIT.models import ExpenditureCategory, ProgrammeCode


class ExpenditureTypeForm(forms.Form):
    expenditure_category = forms.ModelChoiceField(
        queryset=ExpenditureCategory.objects.all(),
        widget=Select(),
    )


class ProgrammeForm(forms.Form):
    programme_code = forms.ModelChoiceField(
        queryset=ProgrammeCode.objects.filter(
            active=True,
        ),
        widget=Select(),
    )
