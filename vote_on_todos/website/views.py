from __future__ import annotations

import datetime
from typing import Any

import django.urls
from django import forms
from django import http
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from . import config

# Note [Users are not logged in]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# We have not implemented auth on this site yet, so users are never logged in.


class Lists(LoginRequiredMixin, generic.TemplateView):
    template_name = 'lists.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        queries = config.get_list_queries()

        context = {
            'todo_lists': sorted(
                queries.get_lists(), key=lambda lst: lst.name,
            ),
        }

        return super().get_context_data(**kwargs) | context


class NewListForm(forms.Form):
    list_name = forms.CharField()
    description = forms.CharField(required=False)


class NewList(LoginRequiredMixin, generic.FormView):  # type: ignore[type-arg]
    # TypeError: type 'FormView' is not subscriptable

    form_class = NewListForm
    template_name = 'new-list.html'
    success_url = django.urls.reverse_lazy('lists')

    def form_valid(self, form: NewListForm) -> http.HttpResponse:
        name = form.cleaned_data['list_name']
        description = form.cleaned_data['description']

        application = config.get_new_list_service()
        application.create_new_list(
            name=name,
            description=description,
            created_by='',  # See Note [Users are not logged in]
            created_at=datetime.datetime.now(datetime.UTC),
        )

        messages.success(self.request, f'New todo list created: {name}')

        return super().form_valid(form)


class List(LoginRequiredMixin, generic.TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        list_id = kwargs['list_id']

        list_queries = config.get_list_queries()
        todo_queries = config.get_todo_queries()

        context = {
            'list': list_queries.get_list(list_id),
            'todos': sorted(
                todo_queries.get_list(list_id), key=lambda todo: todo.created_at,
            ),
        }

        return super().get_context_data(**kwargs) | context


class NewTodoForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(required=False)


class NewTodo(LoginRequiredMixin, generic.FormView):  # type: ignore[type-arg]
    # TypeError: type 'FormView' is not subscriptable

    form_class = NewTodoForm
    template_name = 'new-todo.html'

    def setup(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)

        self.list_id = kwargs['list_id']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        list_queries = config.get_list_queries()

        context = {
            'list': list_queries.get_list(self.list_id),
        }

        return super().get_context_data(**kwargs) | context

    def form_valid(self, form: NewListForm) -> http.HttpResponse:
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']

        application = config.get_new_todo_service()
        application.create_new_todo(
            title=title,
            list_id=self.list_id,
            description=description,
            created_by='',  # See Note [Users are not logged in]
            created_at=datetime.datetime.now(datetime.UTC),
        )

        messages.success(self.request, f'New todo created: {title}')

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return django.urls.reverse('list', kwargs={'list_id': self.list_id})
