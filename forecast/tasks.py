from celery import shared_task

from forecast.import_actuals import (
    upload_trial_balance_report,
)

from upload_file.models import FileUpload


@shared_task
def process_uploaded_file(month, year):
    latest_unprocessed = FileUpload.objects.filter(
        processed=False,
    ).order_by('-created').first()

    if latest_unprocessed is not None:
        print("Unprocessed file: {}".format(latest_unprocessed))

        upload_trial_balance_report(
            latest_unprocessed,
            month,
            year,
        )
        # Process file here

        latest_unprocessed.processed = True
        latest_unprocessed.save()
        print("Saved file...")
