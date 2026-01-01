from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('validate/', views.validate_code, name='validate_code'),
    path('board/', views.board, name='board'),
    path('logout/', views.logout_view, name='logout'),
]
