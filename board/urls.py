from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('validate/', views.validate_code, name='validate_code'),
    path('rooms/', views.get_room_list, name='room_list'),
    path('update-room-name/', views.update_room_name, name='update_room_name'),
    path('check-messages/', views.check_new_messages, name='check_messages'),
    path('board/', views.board, name='board'),
    path('task-board/', views.task_board, name='task_board'),
    path('create-task/', views.create_task, name='create_task'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('add-task-update/', views.add_task_update, name='add_task_update'),
    path('logout/', views.logout_view, name='logout'),
]
