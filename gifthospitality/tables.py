from core.tables import FadminTable

from .models import GiftAndHospitality


class GiftHospitalityTable(FadminTable):

    class Meta(FadminTable.Meta):
        model = GiftAndHospitality

        fields = [
            "id",
            "category",
            "classification",
            "group_name",
            "date_received",
            "venue",
            "reason",
            "value",
            "rep",
            "group",
            "grade",
            "offer",
            "company_rep",
            "company",
            "company_other",
            "action_taken",
            "entered_date_stamp",
            "entered_by",
        ]
