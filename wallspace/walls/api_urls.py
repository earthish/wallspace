from django.urls import path
from .views import (
    WallListCreateAPIView
)
urlpatterns = [
    path(
        '',
        WallListCreateAPIView.as_view(),
        name='wall-list'
    ),
]