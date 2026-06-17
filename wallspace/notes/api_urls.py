from django.urls import path
from .views import CreateNoteAPIView, UpdateNoteAPIView, DeleteNoteAPIView

urlpatterns = [
    path(
        'create/',
        CreateNoteAPIView.as_view(),
        name='api-note-create'
    ),
    path(
        '<int:pk>/update/',
        UpdateNoteAPIView.as_view(),
        name='api-note-update'
    ),

    path(
        '<int:pk>/delete/',
        DeleteNoteAPIView.as_view(),
        name='api-note-delete'
    ),
]