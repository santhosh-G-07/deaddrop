from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('validate/', views.validate_code, name='validate_code'),
    path('rooms/', views.get_room_list, name='room_list'),
    path('update-room-name/', views.update_room_name, name='update_room_name'),
    path('check-messages/', views.check_new_messages, name='check_messages'),
    path('board/', views.board, name='board'),
    path('logout/', views.logout_view, name='logout'),
]
