import datetime

from bootstrap_datepicker_plus import DatePickerInput

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import GIFT_OFFERED, GIFT_RECEIVED, GiftAndHospitality


class GiftAndHospitalityReceivedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.offer = GIFT_RECEIVED
        super(GiftAndHospitalityReceivedForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].required = True
        # self.fields["company"].visible = False

        self.fields['classification_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['category_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['date_offered'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['action_taken'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['venue'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['reason'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['value'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['rep_fk'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['grade_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['group_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['company_rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['company_fk'].widget.attrs.update({'class': 'govuk-select'})

    def save(self, *args, **kwargs):
        self.instance.offer = self.offer
        self.instance.entered_date_stamp = datetime.datetime.now()
        if self.instance.group_fk:
            self.instance.group = self.instance.group_fk
            self.instance.group_name = (
                self.instance.group_fk.cost_centre.directorate.group.group_name
            )
        return super(GiftAndHospitalityReceivedForm, self).save(*args, **kwargs)

    class Meta:
        def __init__(self, *args, **kwargs):
            super(GiftAndHospitalityReceivedForm.Meta, self).__init__(*args, **kwargs)

        model = GiftAndHospitality
        fields = [
            "classification_fk",
            "category_fk",
            "date_offered",
            "action_taken",
            "venue",
            "reason",
            "value",
            "rep_fk",
            "grade_fk",
            "group_fk",
            "company_rep",
            "company_fk",
            "company",
        ]
        labels = {
            "company_fk": _("Company received from"),
            "company_rep": _("Company Representative received from"),
            "group_fk": _("DIT Group offered to"),
            "rep_fk": _("DIT Representative offered to"),
            "grade_fk": _("DIT Representative Grade"),
        }

        widgets = {
            # 'rep_fk' : ModelSelect2Bootstrap(url='people-autocomplete'),
            # "rep_fk": autocomplete.ModelSelect2(url="people-autocomplete"),
            "date_offered": DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",  # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }
            ),
        }


class GiftAndHospitalityOfferedForm(GiftAndHospitalityReceivedForm):
    def __init__(self, *args, **kwargs):
        self.offer = GIFT_OFFERED
        super(GiftAndHospitalityReceivedForm, self).__init__(*args, **kwargs)

        self.fields['classification_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['category_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['date_offered'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['action_taken'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['venue'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['reason'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['value'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['rep_fk'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['grade_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['group_fk'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['company_rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['company_fk'].widget.attrs.update({'class': 'govuk-select'})

    class Meta(GiftAndHospitalityReceivedForm.Meta):
        labels = {
            "company_fk": _("Company offered to"),
            "company_rep": _("Company Representative offered to"),
            "group_fk": _("DIT Group received from"),
            "rep_fk": _("DIT Representative received from"),
        }
