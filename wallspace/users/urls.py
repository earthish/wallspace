from django.urls import path
from . import views
from .views import RegisterAPIView

urlpatterns = [
        path('register/',views.register,name='register'),
]
