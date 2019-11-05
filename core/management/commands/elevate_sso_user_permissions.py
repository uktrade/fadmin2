from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Elevate SSO user permissions for local development purposes"

    def handle(self, *args, **options):
        if settings.CAN_ELEVATE_SSO_USER_PERMISSIONS:
            user = get_user_model()
            sso_user = user.objects.exclude(email="AnonymousUser").first()
            sso_user.is_superuser = True
            sso_user.is_staff = True
            sso_user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully elevated user permission for user {}".format(
                        sso_user.email
                    )
                )
            )
        else:
            self.stdout.write(
                self.style.FATAL("You do not have permission to perform this action")
            )
