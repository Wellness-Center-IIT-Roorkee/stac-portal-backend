import requests
from django.contrib.auth import login
from rest_framework import response, permissions, status
from rest_framework.views import APIView

from stac_portal.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_REDIRECT_URI
from base_auth.constants.oauth_urls import GET_ACCESS_TOKEN_URL, \
    GET_USER_DATA_URL
from base_auth.models import User, Student, Faculty
from base_auth.serializers.user import UserSerializer
from base_auth.utils import update_or_create_student

# TODO: Log all the errors encountered

class LoginView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        if request.user.is_authenticated:
            response_data = {
                'error': 'You are already logged in.',
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        try:
            # Get access token from channel i
            code = data['code']
            token_request = {
                'client_id': OAUTH_CLIENT_ID,
                'client_secret': OAUTH_CLIENT_SECRET,
                'grant_type': "authorization_code",
                'redirect_uri': OAUTH_REDIRECT_URI,
                'code': code
            }
            token_response = requests.post(
                GET_ACCESS_TOKEN_URL,
                data=token_request
            )
            if token_response.status_code in range(200, 300):
                # Get user data in exchange of access token
                token_response_data = token_response.json()
                access_token = token_response_data.get('access_token')
                auth_header = f"Bearer {access_token}"
                headers = {'Authorization': auth_header}
                user_data_response = requests.get(
                    GET_USER_DATA_URL,
                    headers=headers
                )
                if user_data_response.status_code in range(200, 300):
                    user_data = user_data_response.json()
                    person = user_data.get('person')
                    student = user_data.get('student')
                    contact_information = user_data.get('contactInformation')
                    roles = person.get('roles')
                    person_roles = [role['role'] for role in roles if role['activeStatus'] == 'ActiveStatus.IS_ACTIVE']

                    # Only users with student or faculty role can login using channel i
                    if 'Student' not in person_roles and 'FacultyMember' not in person_roles:
                        response_data = {
                            'error': 'Invalid role',
                        }
                        return response.Response(
                            data=response_data,
                            status=status.HTTP_403_FORBIDDEN
                        )

                    institute_email = contact_information.get(
                        'instituteWebmailAddress'
                    )
                    phone_number = contact_information.get(
                        'primaryPhoneNumber'
                    )
                    name = person.get('fullName')
                    display_picture = person.get('displayPicture')
                    user_object = {
                        'name': name,
                        'email': institute_email,
                        'phone_number': phone_number,
                        'display_picture': display_picture,
                        'username': institute_email,
                    }

                    request_user, created = User.objects.get_or_create(
                        email=institute_email,
                        defaults=user_object
                    )

                    if 'Student' in person_roles:
                        try:
                            update_or_create_student(request_user, student)
                        except Exception as e:
                            response_data = {
                                'error': 'Unable to create student profile.',
                            }
                            return response.Response(
                                data=response_data,
                                status=status.HTTP_404_NOT_FOUND
                            )

                    elif 'FacultyMember' in person_roles:
                        Faculty.objects.create(user=request_user)

                    login(request, request_user)
                    user_serializer = UserSerializer(request_user)
                    return response.Response(
                        data=user_serializer.data,
                        status=status.HTTP_200_OK
                    )

                else:
                    response_data = {
                        'error': 'Unable to fetch data.',
                    }
                    return response.Response(
                        data=response_data,
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                response_data = {
                    'error': 'Unable to fetch data.',
                }
                return response.Response(
                    data=response_data,
                    status=status.HTTP_404_NOT_FOUND
                )

        except KeyError:
            response_data = {
                'error': 'Bad request.',
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
