from django.db.models import Q
from rest_framework import permissions, viewsets, status, response
from rest_framework.decorators import action

from base_auth.constants import ADMIN, FACULTY, STUDENT
from stac_application.constants import APPROVED, PENDING, REJECTED, INCOMPLETE
from stac_application.models import Application
from stac_application.permissions import StacPermission, IsAdminOrIsFaculty
from stac_application.serializers import (
    AdminApplicationShortSerializer,
    FacultyApplicationShortSerializer,
    StudentApplicationShortSerializer,
    AdminApplicationDetailSerializer,
    FacultyApplicationDetailSerializer,
    StudentApplicationDetailSerializer,
)
from stac_application.utils.send_email import send_email_async
from stac_application.utils.email_templates import get_new_application_mail, \
    get_update_application_mail


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StacPermission]

    def get_queryset(self):
        user = self.request.user
        role = user.get_role()
        queryset = Application.objects.none()
        if role == STUDENT:
            queryset = Application.objects.filter(student=user.student)
        elif role == FACULTY:
            queryset = Application.objects.filter(
                Q(hod_email=user.email) | Q(supervisor_email=user.email)
            )
        elif role == ADMIN:
            queryset = Application.objects.all()

        return queryset

    def get_serializer_class(self):
        action = self.action
        user = self.request.user
        role = None
        if hasattr(user, 'get_role'):
            role = user.get_role()

        serializer_map = {
            STUDENT: {
                'list': StudentApplicationShortSerializer,
                **dict.fromkeys(
                    ['create', 'retrieve', 'update', 'partial_update'],
                    StudentApplicationDetailSerializer
                ),
            },
            FACULTY: {
                'list': FacultyApplicationShortSerializer,
                'retrieve': FacultyApplicationDetailSerializer,
            },
            ADMIN: {
                'list': AdminApplicationShortSerializer,
                'retrieve': AdminApplicationDetailSerializer,
            }
        }

        try:
            serializer_class = serializer_map[role][action]
            return serializer_class
        except KeyError:
            return StudentApplicationShortSerializer

    def get_serializer_context(self):
        context = super(ApplicationViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        data = request.data
        miscellaneous_documents = data.pop('miscellaneous_documents', None)
        request.data._mutable = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        student = user.student
        serializer.save(student=student)

        application = Application.objects.get(id=serializer.data['id'])
        if miscellaneous_documents:
            for document in miscellaneous_documents:
                application.miscellaneous_documents.create(document=document)

        email_body = get_new_application_mail(application)
        email_subject = 'Application received through StAC portal'
        if application.hod_email:
            send_email_async(subject=email_subject, body=email_body,
                             to=[application.hod_email, ])
        if application.supervisor_email:
            send_email_async(subject=email_subject, body=email_body,
                             to=[application.supervisor_email, ])

        return response.Response(serializer.data,
                                 status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.supervisor_approval_status = PENDING
        instance.hod_approval_status = PENDING
        instance.admin_approval_status = PENDING
        instance.save()

        request.data._mutable = True
        data = request.data
        miscellaneous_documents = data.pop('miscellaneous_documents', None)
        request.data._mutable = False

        if miscellaneous_documents:
            for document in miscellaneous_documents:
                instance.miscellaneous_documents.create(document=document)

        email_body = get_update_application_mail(instance)
        email_subject = 'Application updated through StAC portal'
        if instance.hod_email:
            send_email_async(subject=email_subject, body=email_body,
                             to=[instance.hod_email, ])
        if instance.supervisor_email:
            send_email_async(subject=email_subject, body=email_body,
                             to=[instance.supervisor_email, ])

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAdminOrIsFaculty])
    def change_status(self, request, pk=None):
        user = request.user
        application_instance = self.get_object()
        application_status = request.data.get('status')
        allowed_status = [APPROVED, PENDING, REJECTED, INCOMPLETE]

        if not status:
            return response.Response(
                {'error': 'Status field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if application_status not in allowed_status:
            return response.Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        role = user.get_role()
        if role == FACULTY:
            if user.email == application_instance.hod_email:
                application_instance.hod_approval_status = application_status
            if user.email == application_instance.supervisor_email:
                application_instance.supervisor_approval_status = application_status
        elif role == ADMIN:
            application_instance.admin_approval_status = application_status
            remarks = request.data.get('remarks')
            application_instance.remarks = remarks

        application_instance.save()
        return response.Response(
            {'message': 'Status Updated Successfully'},
            status=status.HTTP_200_OK
        )
