import boto3

from celery import shared_task

from django.conf import settings

from core.myutils import run_anti_virus

from forecast.import_actuals import upload_trial_balance_report
from forecast.import_budgets import upload_budget_from_file

from upload_file.models import FileUpload


@shared_task
def process_uploaded_file(*args):
    latest_unprocessed = FileUpload.objects.filter(
        status=FileUpload.UNPROCESSED,
    ).order_by('-created').first()

    if latest_unprocessed is not None:
        latest_unprocessed.status = FileUpload.ANTIVIRUS
        latest_unprocessed.save()

        s3 = boto3.resource('s3')

        obj = s3.Object(
            settings.AWS_STORAGE_BUCKET_NAME,
            latest_unprocessed.document_file.name,
        )
        file_body = obj.get()['Body'].read()

        # Check for viruses
        anti_virus_result = run_anti_virus(
            file_body,
        )

        if anti_virus_result["malware"]:
            latest_unprocessed.status = FileUpload.ERROR
            latest_unprocessed.user_error_message = "A virus was found in the file"
            latest_unprocessed.error_message = str(anti_virus_result)
            latest_unprocessed.save()
        else:
            latest_unprocessed.status = FileUpload.PROCESSING
            latest_unprocessed.save()
            # Process file here
            if latest_unprocessed.document_type == FileUpload.ACTUALS:
                success = upload_trial_balance_report(
                    latest_unprocessed,
                    *args
                )
            if latest_unprocessed.document_type == FileUpload.BUDGET:
                success = upload_budget_from_file(
                    latest_unprocessed,
                    *args
                )

            if success:
                latest_unprocessed.status = FileUpload.PROCESSED
                latest_unprocessed.save()
