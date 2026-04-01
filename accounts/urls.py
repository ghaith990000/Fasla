from django.urls import path
from .views import register, profile, logout

urlpatterns = [
    path("register/", register),
    path("profile/", profile),
    path("logout/", logout),
]