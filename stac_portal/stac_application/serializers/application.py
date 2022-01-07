from rest_framework import serializers

from base_auth.constants import FACULTY
from stac_application.constants import NOT_AVAILABLE
from stac_application.models import Application
from stac_application.serializers.student import StudentShortSerializer, StudentDetailSerializer


class AdminApplicationShortSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'submission_time',
            'supervisor_approval_status',
            'admin_approval_status',
            'hod_approval_status'
        ]

    def get_student(self, instance):
        student_serializer = StudentShortSerializer(instance=instance.student)
        return student_serializer.data


class FacultyApplicationShortSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'student', 'submission_time', 'status']

    def get_student(self, instance):
        student_serializer = StudentShortSerializer(instance=instance.student)
        return student_serializer.data

    def get_status(self, instance):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if hasattr(user, 'get_role') and user.get_role() == FACULTY:
            if user.email == instance.supervisor_email:
                return instance.supervisor_approval_status
            if user.email == instance.hod_email:
                return instance.hod_approval_status
        return NOT_AVAILABLE


class StudentApplicationShortSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='admin_approval_status', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'submission_time', 'status']


class AdminApplicationDetailSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = '__all__'

    def get_student(self, instance):
        student_serializer = StudentDetailSerializer(instance=instance.student)
        return student_serializer.data


class FacultyApplicationDetailSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Application
        exclude = ['hod_approval_status', 'admin_approval_status', 'supervisor_approval_status', 'remarks']

    def get_student(self, instance):
        student_serializer = StudentDetailSerializer(instance=instance.student)
        return student_serializer.data

    def get_status(self, instance):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if hasattr(user, 'get_role') and user.get_role() == FACULTY:
            if user.email == instance.supervisor_email:
                return instance.supervisor_approval_status
            if user.email == instance.hod_email:
                return instance.hod_approval_status
        return NOT_AVAILABLE


class StudentApplicationDetailSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(read_only=True)
    status = serializers.CharField(source='admin_approval_status', read_only=True)
    remarks = serializers.CharField(read_only=True)

    class Meta:
        model = Application
        exclude = ['hod_approval_status', 'admin_approval_status', 'supervisor_approval_status']

    def get_student(self, instance):
        student_serializer = StudentDetailSerializer(instance=instance.student)
        return student_serializer.data
