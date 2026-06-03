from django.urls import path
from . import views

urlpatterns = [
    path(
        'update-position/',
        views.update_position,
        name='update-position'
    ),
]