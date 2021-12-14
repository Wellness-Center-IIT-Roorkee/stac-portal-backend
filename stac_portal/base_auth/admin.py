from django.contrib import admin

from base_auth.models import Admin, Faculty, Student, User


admin.site.register(Admin)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(User)
