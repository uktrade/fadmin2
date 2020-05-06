from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from download_file.views.mi_report_download import DownloadMIReportView
from download_file.views.oscar_return import DownloadOscarReturnView

from core.test.test_base import RequestFactoryBase


class DownloadViewTests(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

    def test_download_mi_view(self):
        assert not self.test_user.has_perm("forecast.can_download_mi_reports")

        downloaded_files_url = reverse("download_mi_report",)

        # Should have been redirected (no permission)
        with self.assertRaises(PermissionDenied):
            self.factory_get(
                downloaded_files_url, DownloadMIReportView,
            )

        can_download_files = Permission.objects.get(codename="can_download_mi_reports",)
        self.test_user.user_permissions.add(can_download_files)
        self.test_user.save()

        resp = self.factory_get(downloaded_files_url, DownloadMIReportView,)

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)

    def test_download_oscar_view(self):
        assert not self.test_user.has_perm("forecast.can_download_oscar")

        downloaded_files_url = reverse("download_oscar_report",)

        # Should have been redirected (no permission)
        with self.assertRaises(PermissionDenied):
            self.factory_get(
                downloaded_files_url, DownloadOscarReturnView,
            )

        can_download_files = Permission.objects.get(codename="can_download_oscar",)
        self.test_user.user_permissions.add(can_download_files)
        self.test_user.save()

        resp = self.factory_get(downloaded_files_url, DownloadOscarReturnView,)

        # Should have been permission now
        self.assertEqual(resp.status_code, 200)
