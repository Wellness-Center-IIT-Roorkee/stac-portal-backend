from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stac_application.views.application import ApplicationViewSet

router = DefaultRouter()
router.register(r'application', ApplicationViewSet, basename='Application')

urlpatterns = [
    path('', include(router.urls)),
]
