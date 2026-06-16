from django.urls import path
from .views import RegisterAPIView, ProfileAPIView
urlpatterns = [
    path('register/',RegisterAPIView.as_view(),name='api-register'),
    path(
        'register/',
        RegisterAPIView.as_view(),
        name='api-register'
    ),

    path(
        'profile/',
        ProfileAPIView.as_view(),
        name='api-profile'
    ),
]