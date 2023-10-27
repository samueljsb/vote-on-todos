from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path('lists/', views.Lists.as_view(), name='lists'),
]
