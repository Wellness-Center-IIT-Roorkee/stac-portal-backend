from django.db import models

from base_auth.models import User


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student'
    )

    enrollment_number = models.CharField(
        max_length=15,
        default=None,
    )

    branch = models.CharField(
        max_length=127,
        default=None,
    )

    department = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        default=None,
    )

    degree = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        default=None,
    )

    current_year = models.IntegerField()

    current_semester = models.IntegerField()

    def __str__(self):
        user = self.user
        return f"{user.email} - {user.name}"
