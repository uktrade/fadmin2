from core.tables import FadminTable

from .models import GiftAndHospitality


class GiftHospitalityTable(FadminTable):
    # id = tables.Column(
    #     verbose_name="id", accessor="directorate.group.group_code"
    # )

    class Meta(FadminTable.Meta):
        model = GiftAndHospitality

        fields = (
            "id",
            "category",
            "classification",
            "group_name",
            "date_offered",
            "venue",
            "reason",
            "value",
            "rep",
            "group",
            "grade",
            "offer",
            "company_rep",
            "company",
            "action_taken",
            "entered_date_stamp",
            "entered_by",
        )

        def __init__(self, *args, **kwargs):
            super(GiftHospitalityTable, self).__init__(*args, **kwargs)
            for f in self.fields:
                self.fields[f].required = True
            # self.fields["company"].visible = False

            self.fields['classification'].widget.attrs.update({'class': 'govuk-select'})
            self.fields['category'].widget.attrs.update({'class': 'govuk-select'})
            self.fields['date_offered']
            self.fields['action_taken'].widget.attrs.update({'class': 'govuk-select'})
            self.fields['venue'].widget.attrs.update({'class': 'govuk-input'})
            self.fields['reason'].widget.attrs.update({'class': 'govuk-input'})
            self.fields['value'].widget.attrs.update({'class': 'govuk-input'})
            self.fields['rep'].widget.attrs.update({'class': 'govuk-input'})
            self.fields['grade'].widget.attrs.update({'class': 'govuk-select'})
            self.fields['group'].widget.attrs.update({'class': 'govuk-select'})
            self.fields['company_rep'].widget.attrs.update({'class': 'govuk-input'})
            self.fields['company'].widget.attrs.update({'class': 'govuk-select'})

# class GiftHospitalityForm(forms.ModelForm):
#     class Meta:
#         model = GiftAndHospitality
#         fields = (
#             "id",
#             "category",
#             "classification",
#             "group_name",
#             "date_offered",
#             "venue",
#             "reason",
#             "value",
#             "rep",
#             "group",
#             "grade",
#             "offer",
#             "company_rep",
#             "company",
#             "action_taken",
#             "entered_date_stamp",
#             "entered_by",
#         )
