from django.urls import path
from .views import CreateNoteAPIView, UpdateNoteAPIView

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
]