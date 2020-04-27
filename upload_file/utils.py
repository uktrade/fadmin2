from upload_file.models import FileUpload


def set_file_upload_error(file_upload, user_error, error):
    file_upload.status = FileUpload.ERROR
    file_upload.user_error_message = user_error
    file_upload.error_message = error
    file_upload.save()

def set_file_upload_feedback(file_upload, feedback):
    file_upload.status = FileUpload.PROCESSING
    file_upload.user_error_message = feedback
    file_upload.save()

def set_incremental_file_upload_error(file_upload, user_error, error):
    file_upload.status = FileUpload.ERROR
    file_upload.user_error_message = file_upload.user_error_message  + user_error
    file_upload.error_message = error
    file_upload.save()
