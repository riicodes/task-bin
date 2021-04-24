from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('task/new/', views.create, name='create'),
    path('task/current/', views.current, name='current'),
    path('task/completed/', views.completed, name='completed'),

    path('task/<int:pk>/', views.detail, name='detail'),
    path('task/<int:pk>/complete/', views.complete, name='complete'),
    path('task/<int:pk>/delete', views.delete, name='delete'),
]
