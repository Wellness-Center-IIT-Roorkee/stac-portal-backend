from django.db import models
from django.utils.translation import gettext as _

from base_auth.models import Student
from stac_application.constants import APPROVAL_STATUS, PENDING, SEMESTERS
from stac_application.utils import UploadTo


class Application(models.Model):
    """
    Model to store information about the Stac Application filled by a student
    """

    student = models.ForeignKey(
        to=Student,
        related_name='applications',
        on_delete=models.CASCADE,
    )

    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        default=None,
    )

    applied_semester = models.CharField(
        _('applied semester'),
        max_length=7,
        choices=SEMESTERS,
    )

    supervisor_email = models.EmailField(_('supervisor email'),)

    hod_email = models.EmailField(_('HOD email'), )

    supervisor_approval_status = models.CharField(
        _('supervisor approval status'),
        max_length=7,
        choices=APPROVAL_STATUS,
        default=PENDING
    )

    hod_approval_status = models.CharField(
        _('HOD approval status'),
        max_length=3,
        choices=APPROVAL_STATUS,
        default=PENDING
    )

    admin_approval_status = models.CharField(
        _('admin approval status'),
        max_length=3,
        choices=APPROVAL_STATUS,
        default=PENDING
    )

    application_form = models.FileField(
        _('application form'),
        upload_to=UploadTo('application-forms/%Y')
    )

    extension_letter = models.FileField(
        _('extension letter'),
        upload_to=UploadTo('extension-letters/%Y')
    )

    academic_summary = models.FileField(
        _('academic summary'),
        upload_to=UploadTo('academic-summaries/%Y')
    )

    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        student = self.student
        submission_time = self.submission_time
        return f'Application - {student} - {submission_time}'
