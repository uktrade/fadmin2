from celery import shared_task

from forecast.models import FileUpload


@shared_task
def process_uploaded_file():
    latest_unprocessed = FileUpload.objects.filter(
        processed=False,
    ).order_by('-created').first()

    if latest_unprocessed is not None:
        print("Unprocessed file: {}".format(latest_unprocessed))
        # Process file here
        latest_unprocessed.processed = True
        latest_unprocessed.save()
        print("Saved file...")
