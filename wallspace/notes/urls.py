from django.urls import path
from . import views

urlpatterns = [
    path(
        'update-position/',
        views.update_position,
        name='update-position'
    ),

    path('delete/<int:note_id>/',
    views.delete_note,
    name='delete-note'
    ),

    path(
    'edit/<int:note_id>/',
    views.edit_note,
    name='edit-note'
    ),

]