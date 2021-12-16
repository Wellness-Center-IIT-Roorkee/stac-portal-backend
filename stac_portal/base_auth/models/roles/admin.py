from django.db import models

from base_auth.models import User


class Admin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='admin',
    )

    def __str__(self):
        user = self.user
        return f"{user.email} - {user.name}"
