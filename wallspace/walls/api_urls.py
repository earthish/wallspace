from django.urls import path
from .views import (
    
    WallListAPIView,
    CreateWallAPIView,
    WallDetailAPIView,
    UpdateWallAPIView


)
urlpatterns = [
    
    path(
        '',
        WallListAPIView.as_view(),
        name='api-wall-list'
    ),

    path(
        'create/',
        CreateWallAPIView.as_view(),
        name='api-wall-create'
    ),
    path(
        '<int:pk>/',
        WallDetailAPIView.as_view(),
        name='api-wall-detail'
    ),
    path(
        '<int:pk>/update/',
        UpdateWallAPIView.as_view(),
        name='api-wall-update'
    ),
]