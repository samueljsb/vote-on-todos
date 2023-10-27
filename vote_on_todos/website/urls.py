from __future__ import annotations

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('lists/', views.Lists.as_view(), name='lists'),
    path('lists/<list_id>/', views.List.as_view(), name='list'),
    path('new-list/', views.NewList.as_view(), name='new-list'),
    path('new-todo/<list_id>/', views.NewTodo.as_view(), name='new-todo'),
]
