
from django import forms


class EditForm(forms.Form):
    cell_data = forms.Textarea()
