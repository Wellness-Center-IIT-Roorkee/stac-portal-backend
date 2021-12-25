from rest_framework import serializers


class StudentShortSerializer(serializers.BaseSerializer):
    """
    A read only serializer for brief description of Student model
    """

    def to_representation(self, instance):
        return{
            'name': instance.user.name,
            'email': instance.user.email,
            'enrollment_number': instance.enrollment_number,
        }


class StudentDetailSerializer(serializers.BaseSerializer):
    """
    A read only serializer for detailed description of Student model
    """

    def to_representation(self, instance):
        return{
            'name': instance.user.name,
            'email': instance.user.email,
            'enrollment_number': instance.enrollment_number,
            'branch': instance.branch,
            'department': instance.department,
        }
