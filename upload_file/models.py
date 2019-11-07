from django.db import models

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

    def __str__(self):
        return "{} {}".format(
            self.document_file,
            self.status,
        )
