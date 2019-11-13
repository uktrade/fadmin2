from django.db import models
from django.contrib.auth import get_user_model

from pathlib import Path

from core.metamodels import (
    SimpleTimeStampedModel,
)


class FileUpload(SimpleTimeStampedModel):
    UNPROCESSED = 'unprocessed'
    PROCESSING = 'processing'
    PROCESSED = 'processed'
    ERROR = 'error'

    STATUS_CHOICES = [
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSING, 'Processing'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    ]

    document_file = models.FileField(
        upload_to='uploaded/actuals/'
    )
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default=UNPROCESSED,
    )
    user_error_message = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    error_message = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    uploading_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    @property
    def file_name(self):
        return Path(
            self.document_file.path,
        ).name

    def __str__(self):
        return "{} {}".format(
            self.document_file,
            self.status,
        )


class UploadPermission(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    upload_actuals = models.BooleanField(
        default=False,
    )
    upload_budget = models.BooleanField(
        default=False,
    )
