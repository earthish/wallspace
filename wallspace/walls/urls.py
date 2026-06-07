from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('wall/<int:pk>/',views.wall_detail,name='wall-detail'),
    path('wall/<int:pk>/delete/', views.delete_wall, name='delete-wall'),
    path('wall/<int:wall_id>/remove-member/<int:member_id>/',
    views.remove_member,
    name='remove-member'),
    path('wall/<int:wall_id>/toggle-role/<int:member_id>/',
    views.toggle_role,
    name='toggle-role'),

]
