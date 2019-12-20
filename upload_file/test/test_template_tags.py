from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from upload_file.templatetags.upload_permissions import (
    has_upload_permission,
)


class UploadPermissionTestTestCase(TestCase):
    def test_has_upload_permission(self):
        test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        assert not has_upload_permission(test_user)

        can_upload_files = Permission.objects.get(
            name='forecast.can_upload_files',
        )
        self.test_user_permissions.add(can_upload_files)
        self.test_user.save()

        assert has_upload_permission(test_user) is True
