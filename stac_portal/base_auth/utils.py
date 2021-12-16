from base_auth.models import Student
from base_auth.serializers.roles.student import StudentSerializer


def update_or_create_student(user, student_dict):
    """
    Utility function to create or update a student
    :param user: User object
    :param student_dict: dictionary of student details received from channel i
    :return:
    """
    enrollment_number = student_dict.get('enrolmentNumber')
    branch = student_dict.get('branch name')
    degree = student_dict.get('branch degree name')
    department = student_dict.get('branch department name')
    current_year = student_dict.get('currentYear')
    current_semester = student_dict.get('currentSemester')
    student_object = {
        'enrollment_number': enrollment_number,
        'branch': branch,
        'degree': degree,
        'department': department,
        'current_year': current_year,
        'current_semester': current_semester,
    }
    student_serializer = StudentSerializer(
        data=student_object
    )
    student_serializer.is_valid(raise_exception=True)
    Student.objects.update_or_create(user=user, defaults=student_serializer.validated_data)
