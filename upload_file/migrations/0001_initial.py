# Generated by Django 2.2.10 on 2020-05-22 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleHistoryFileUpload',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('document_type', models.CharField(choices=[('actuals', 'Actuals'), ('budget', 'Budget')], default='actuals', max_length=100)),
                ('document_file', models.TextField(max_length=1000)),
                ('status', models.CharField(choices=[('unprocessed', 'Unprocessed'), ('antivirus', 'Checking for viruses'), ('processed_error', 'Processed. Not uploaded, error(s) found.'), ('processed_warning', 'Processed. Uploaded, warning(s) found.'), ('processing', 'Processing'), ('parsing', 'Processing after error'), ('processed', 'Processed and uploaded.'), ('error', 'Fatal error.')], default='unprocessed', max_length=100)),
                ('user_error_message', models.TextField(blank=True, null=True)),
                ('user_warning_message', models.TextField(blank=True, null=True)),
                ('row_process_message', models.CharField(blank=True, max_length=255, null=True)),
                ('error_message', models.CharField(blank=True, max_length=255, null=True)),
                ('error_count', models.IntegerField(blank=True, default=0, null=True)),
                ('warning_count', models.IntegerField(blank=True, default=0, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('uploading_user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical file upload',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('document_type', models.CharField(choices=[('actuals', 'Actuals'), ('budget', 'Budget')], default='actuals', max_length=100)),
                ('document_file', models.FileField(max_length=1000, upload_to='')),
                ('status', models.CharField(choices=[('unprocessed', 'Unprocessed'), ('antivirus', 'Checking for viruses'), ('processed_error', 'Processed. Not uploaded, error(s) found.'), ('processed_warning', 'Processed. Uploaded, warning(s) found.'), ('processing', 'Processing'), ('parsing', 'Processing after error'), ('processed', 'Processed and uploaded.'), ('error', 'Fatal error.')], default='unprocessed', max_length=100)),
                ('user_error_message', models.TextField(blank=True, null=True)),
                ('user_warning_message', models.TextField(blank=True, null=True)),
                ('row_process_message', models.CharField(blank=True, max_length=255, null=True)),
                ('error_message', models.CharField(blank=True, max_length=255, null=True)),
                ('error_count', models.IntegerField(blank=True, default=0, null=True)),
                ('warning_count', models.IntegerField(blank=True, default=0, null=True)),
                ('uploading_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_upload_admin', 'Can upload in Admin')],
            },
        ),
    ]
