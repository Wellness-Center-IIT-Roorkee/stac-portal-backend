from django.db import models

from base_auth.models import User


class Faculty(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='faculty',
    )
