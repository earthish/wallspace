from django.urls import path
from .views import (
    
    WallListAPIView,
    CreateWallAPIView

)
urlpatterns = [
    
    path(
        '',
        WallListAPIView.as_view(),
        name='wall-list'
    ),

    path(
        'create/',
        CreateWallAPIView.as_view(),
        name='wall-create'
    ),
]