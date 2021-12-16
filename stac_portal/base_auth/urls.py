from django.urls import path

from base_auth.views.login import LoginView
from base_auth.views.logout import LogoutView
from base_auth.views.who_am_i import WhoAmIView

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'who_am_i/',
        WhoAmIView.as_view(),
        name='who_am_i'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]
