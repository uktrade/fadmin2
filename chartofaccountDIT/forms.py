
from django import forms
from django.forms import Select

from chartofaccountDIT.models import (
    ExpenditureCategory,
    ProgrammeCode,
    ProjectCode,
)


class ExpenditureTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        expenditure_category = kwargs.pop('expenditure_category')

        super(ExpenditureTypeForm, self).__init__(
            *args,
            **kwargs,
        )
        self.fields['expenditure_category'] = forms.ModelChoiceField(
            queryset=ExpenditureCategory.objects.all(),
            widget=Select(),
            initial=expenditure_category
        )
        self.fields['expenditure_category'].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )


class ProgrammeForm(forms.Form):
    programme_code = forms.ModelChoiceField(
        queryset=ProgrammeCode.objects.filter(
            active=True,
        ),
        widget=Select(),
    )
    programme_code.widget.attrs.update(
        {
            "class": "govuk-select",
        }
    )


class ProjectForm(forms.Form):
    project_code = forms.ModelChoiceField(
        queryset=ProjectCode.objects.filter(
            active=True,
        ),
        widget=Select(),
    )
    project_code.widget.attrs.update(
        {
            "class": "govuk-select",
        }
    )
