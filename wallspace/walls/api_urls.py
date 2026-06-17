from django.urls import path
from .views import (
    WallListAPIView,
    CreateWallAPIView,
    WallDetailAPIView,
    UpdateWallAPIView,
    DeleteWallAPIView,
    InviteMemberAPIView,
    ToggleRoleAPIView
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
    path(
        '<int:pk>/delete/',
        DeleteWallAPIView.as_view(),
        name='api-wall-delete'
    ),
    path(
        '<int:pk>/invite/',
        InviteMemberAPIView.as_view(),
        name='api-invite-member'
    ),
    path(
        '<int:wall_id>/members/<int:member_id>/toggle-role/',
        ToggleRoleAPIView.as_view(),
        name='api-toggle-role'
    ),
]