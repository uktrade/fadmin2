from django.db import models

from core.metamodels import (
    SimpleTimeStampedModel,
)


class FileUpload(SimpleTimeStampedModel):
    document_file = models.FileField(
        upload_to='uploaded/actuals/'
    )
    processed = models.BooleanField(
        default=False,
    )

    def __str__(self):
        if self.processed:
            status = "processed"
        else:
            status = "unprocessed"

        return "{} {}".format(
            self.document_file,
            status,
        )
