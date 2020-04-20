from core.tables import FadminTable
import django_tables2 as tables

from .models import GiftAndHospitality

from django import forms


class GiftHospitalityTable(FadminTable):
    id = tables.Column(
        verbose_name="id", accessor="directorate.group.group_code"
    )

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
