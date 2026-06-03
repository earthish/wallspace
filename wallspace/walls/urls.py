from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('wall/<int:pk>/',views.wall_detail,name='wall-detail'),

]