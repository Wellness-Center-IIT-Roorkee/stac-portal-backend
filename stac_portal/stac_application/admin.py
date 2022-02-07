from django.contrib import admin

from stac_application.models import Application, MiscellaneousDocument

# Register your models here.
admin.site.register(Application)
admin.site.register(MiscellaneousDocument)
