from __future__ import annotations

from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='lists/')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('lists/', views.Lists.as_view(), name='lists'),
    path('lists/<list_id>/', views.List.as_view(), name='list'),
    path('new-list/', views.NewList.as_view(), name='new-list'),
    path('new-todo/<list_id>/', views.NewTodo.as_view(), name='new-todo'),
    path('todo/<todo_id>/upvote/', views.UpvoteTodo.as_view(), name='upvote'),
    path(
        'todo/<todo_id>/remove-upvote/', views.RemoveUpvoteFromTodo.as_view(),
        name='remove-upvote',
    ),
]
