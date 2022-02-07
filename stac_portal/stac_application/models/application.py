from django.db import models
from django.core.exceptions import ValidationError
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
        blank=True,
        null=True,
        default=None,
    )

    applied_semester = models.CharField(
        _('applied semester'),
        max_length=7,
        choices=SEMESTERS,
    )

    supervisor_email = models.EmailField(
        _('supervisor email'),
        blank=True,
        null=True,
    )

    hod_email = models.EmailField(
        _('HOD email'),
        blank=True,
        null=True,
    )

    supervisor_approval_status = models.CharField(
        _('supervisor approval status'),
        max_length=7,
        choices=APPROVAL_STATUS,
        default=PENDING,
        blank=True,
    )

    hod_approval_status = models.CharField(
        _('HOD approval status'),
        max_length=3,
        choices=APPROVAL_STATUS,
        default=PENDING,
        blank=True,
    )

    admin_approval_status = models.CharField(
        _('admin approval status'),
        max_length=3,
        choices=APPROVAL_STATUS,
        default=PENDING,
        blank=True,
    )

    application_form = models.FileField(
        _('application form'),
        upload_to=UploadTo('application-forms/%Y'),
    )

    extension_letter = models.FileField(
        _('extension letter'),
        upload_to=UploadTo('extension-letters/%Y'),
        blank=True,
        null=True,
    )

    bank_statement = models.FileField(
        _('bank statement'),
        upload_to=UploadTo('bank-statements/%Y'),
        blank=True,
        null=True,
    )

    itr_form = models.FileField(
        _('itr form'),
        upload_to=UploadTo('itr-forms/%Y'),
        blank=True,
        null=True,
    )

    academic_summary = models.FileField(
        _('academic summary'),
        upload_to=UploadTo('academic-summaries/%Y'),
        blank=True,
        null=True,
    )

    submission_time = models.DateTimeField(
        _('submission time'),
        auto_now_add=True,
    )

    remarks = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        ordering = ['-submission_time']

    def __str__(self):
        student = self.student
        submission_time = self.submission_time
        return f'Application - {student} - {submission_time}'

    def clean(self):
        super(Application, self).clean()
        error_dict = {}
        if 'ph.d.' in self.student.branch.lower():
            if not self.supervisor_email:
                error_dict['supervisor_email'] = ValidationError(
                    _('Missing Supervisor email.'), code='required')
            if not self.hod_email:
                error_dict['hod_email'] = ValidationError(_('HOD email.'),
                                                          code='required')

            if bool(error_dict):
                raise ValidationError(error_dict)

    def save(self, **kwargs):
        self.clean()
        return super(Application, self).save(**kwargs)


class MiscellaneousDocument(models.Model):
    """
    Model to store miscellaneous documents for an application
    """

    application = models.ForeignKey(
        to=Application,
        related_name='miscellaneous_documents',
        on_delete=models.CASCADE,
    )

    document = models.FileField(
        _('document'),
        upload_to=UploadTo('miscellaneous-documents/%Y'),
    )

    def __str__(self):
        application = self.application
        return f'Miscellaneous Document {self.id} - {application}'
