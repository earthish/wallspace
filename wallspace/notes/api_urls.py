from django.urls import path
from .views import CreateNoteAPIView

urlpatterns = [
    path(
        'create/',
        CreateNoteAPIView.as_view(),
        name='api-note-create'
    ),   
]