from rest_framework import serializers

from base_auth.models import User, Student
from base_auth.constants.roles import STUDENT
from base_auth.serializers.roles.student import StudentSerializer


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role', read_only=True)

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'phone_number',
            'display_picture',
            'role',
        ]

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        # Add a student attribute to the serializer representation if user has a student role
        if instance.get_role() == STUDENT:
            student = Student.objects.get(user=instance)
            student_serializer = StudentSerializer(instance=student)
            representation['student'] = student_serializer.data

        return representation
