from core.metamodels import LogChangeModel, TimeStampedModel

from django.db import models

from payroll.models import DITPeople, Grade


class GiftAndHospitalityClassification(TimeStampedModel, LogChangeModel):
    GIFT = 'Gift'
    HOSPITALITY = 'Hospitality'
    GF_TYPE = (
        (GIFT, 'Gift'),
        (HOSPITALITY, 'Hospitality'))

    gift_type = models.CharField(max_length=20,
                                 choices=GF_TYPE, default=HOSPITALITY,
                                 verbose_name='Type')
    gif_hospitality_classification = models.CharField('Classification', max_length=100)
    sequence_no = models.IntegerField(null=True)

    def __str__(self):
        return str(self.gif_hospitality_classification)

    class Meta:
        verbose_name = "Gift and Hospitality Type"
        verbose_name_plural = "Gift and Hospitality Types"
        ordering = ['sequence_no']


class GiftAndHospitalityCategory(TimeStampedModel, LogChangeModel):
    gif_hospitality_category = models.CharField('Category', max_length=100)
    sequence_no = models.IntegerField(null=True)

    def __str__(self):
        return str(self.gif_hospitality_category)

    class Meta:
        verbose_name = "Gift and Hospitality Category"
        verbose_name_plural = "Gift and Hospitality Categories"
        ordering = ['sequence_no']


GIFT_RECEIVED = 'Received'
GIFT_OFFERED = 'Offered'
OFFER_CHOICE = (
    (GIFT_RECEIVED, 'Received by DIT Staff'),
    (GIFT_OFFERED, 'Given by DIT Staff')
)


class GiftAndHospitalityCompany(TimeStampedModel, LogChangeModel):
    gif_hospitality_company = models.CharField('Company', max_length=100)
    sequence_no = models.IntegerField(null=True)

    def __str__(self):
        return str(self.gif_hospitality_company)

    class Meta:
        verbose_name = "Gift and Hospitality Company"
        verbose_name_plural = "Gift and Hospitality Companies"
        ordering = ['sequence_no']

    # Gift and Hospitality


class GiftAndHospitality(LogChangeModel):
    """Model used to keep information of gifts/hospitality received/offered by DIT people.
    On purpose, I am not using foreign key for people and group,
    because we need to have a record of details
    when the gift was registered, not later on."""
    id = models.AutoField('Record ID', primary_key=True)
    old_id = models.IntegerField(null=True, blank=True)
    classification_fk = models.ForeignKey(GiftAndHospitalityClassification,
                                          on_delete=models.PROTECT,
                                          limit_choices_to={'active': True},
                                          verbose_name='Type')

    group_name = models.CharField('Group', max_length=200)
    date_offered = models.DateField('Date of event /  gift offered')
    venue = models.CharField(max_length=1000)
    reason = models.CharField('Description of offer and reason', max_length=1000)
    value = models.IntegerField('Estimated value of offer (£)')
    rep_fk = models.ForeignKey(DITPeople,
                               on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name='DIT Representative')

    rep = models.CharField('DIT representative offered to/from', max_length=255)
    offer = models.CharField(max_length=200, choices=OFFER_CHOICE)
    company_rep = models.CharField('Company representative offered to/from', max_length=200)
    company_fk = models.ForeignKey(GiftAndHospitalityCompany,
                                   on_delete=models.SET_NULL,
                                   limit_choices_to={'active': True},
                                   null=True, blank=True, verbose_name='company')
    company = models.CharField('Company offered to/from', max_length=200)
    ACTION_TYPE = (
        ('Action1', 'Rejected'),
        ('Action2', 'Accepted (difference paid to Department)'),
        ('Action3', 'Accepted (surrendered to Department)'),
        ('Action0', 'Accepted'),
    )
    action_taken = models.CharField(max_length=200,
                                    choices=ACTION_TYPE,
                                    verbose_name='Action taken', blank=True)
    entered_by = models.CharField(max_length=100)
    entered_date_stamp = models.DateField('Date entered')
    category_fk = models.ForeignKey(GiftAndHospitalityCategory,
                                    on_delete=models.PROTECT,
                                    limit_choices_to={'active': True},
                                    verbose_name='category')
    grade_fk = models.ForeignKey(Grade,
                                 on_delete=models.PROTECT,
                                 verbose_name='grade')

    class Meta:
        verbose_name = "Gift and Hospitality"
        verbose_name_plural = "Gift and Hospitality"
        ordering = ['-id']

    def __str__(self):
        return str(self.date_offered)