from django.db.models import Q
from rest_framework import permissions, viewsets, status, response
from rest_framework.decorators import action

from base_auth.constants import ADMIN, FACULTY, STUDENT
from stac_application.constants import APPROVED, PENDING, REJECTED
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

    def create(self, request, *args, **kwargs):
        serializer = StudentApplicationDetailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = request.user
        student = user.student
        serializer.save(student=student)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.supervisor_approval_status = PENDING
        instance.hod_approval_status = PENDING
        instance.admin_approval_status = PENDING
        instance.save()
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsFaculty])
    def change_status(self, request, pk=None):
        user = request.user
        application_instance = self.get_object()
        application_status = request.data.get('status')
        allowed_status = [APPROVED, PENDING, REJECTED]

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

        application_instance.save()
        return response.Response(
            {'message': 'Status Updated Successfully'},
            status=status.HTTP_200_OK
        )
