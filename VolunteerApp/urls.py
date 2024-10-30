from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page route
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create_task/', views.create_task, name='create_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('rewards/', views.rewards, name='rewards'),
    path('base/',views.base, name='base'), 
]

