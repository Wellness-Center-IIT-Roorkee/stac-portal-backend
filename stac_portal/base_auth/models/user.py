from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from base_auth.constants import ADMIN, FACULTY, STUDENT


class User(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField(
        _('name'),
        max_length=127,
    )

    password = models.CharField(
        _('password'),
        max_length=128,
        blank=True,
        null=True,
        default=None,
    )

    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        default=None,
    )

    display_picture = models.URLField(
        blank=True,
        null=True,
    )

    def get_role(self):
        """
        Model method to determine the user roles
        :return: role of the user
        """
        if hasattr(self, STUDENT):
            return STUDENT
        if hasattr(self, FACULTY):
            return FACULTY
        if hasattr(self, ADMIN):
            return ADMIN
        return None

    def __str__(self):
        email = self.email
        name = self.name
        return f"{email} - {name}"
