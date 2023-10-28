from __future__ import annotations

import datetime
from typing import Any

import django.contrib.auth.forms
import django.urls
from django import forms
from django import http
from django.contrib import messages
from django.contrib.auth import models as auth_models
from django.contrib.auth import password_validation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters

from . import config
from vote_on_todos.todos.application import todos as todo_services


# Note [User identification is naive]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# We are currently using usernames to identify users. This is not reasonable (a user
# might change their name) but is a compromise for simplicity for now.


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
            # See Note [User identification is naive]
            created_by=self.request.user.username,  # type: ignore[arg-type]
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

        all_todos = todo_queries.get_list(list_id)
        incomplete_todos = [todo for todo in all_todos if todo.done_at is None]
        completed_todos = [todo for todo in all_todos if todo.done_at is not None]

        context = {
            'list': list_queries.get_list(list_id),
            'incomplete_todos': sorted(
                incomplete_todos,
                key=lambda todo: (-len(todo.upvotes), todo.created_at),
            ),
            'completed_todos': sorted(
                completed_todos,
                key=lambda todo: (todo.done_at, todo.created_at),
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
            # See Note [User identification is naive]
            created_by=self.request.user.username,  # type: ignore[arg-type]
            created_at=datetime.datetime.now(datetime.UTC),
        )

        messages.success(self.request, f'New todo created: {title}')

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return django.urls.reverse('list', kwargs={'list_id': self.list_id})


class UpvoteTodo(LoginRequiredMixin, generic.FormView):  # type: ignore[type-arg]
    # TypeError: type 'FormView' is not subscriptable

    form_class = forms.Form

    def post(
            self, request: http.HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:
        self.todo_id = kwargs['todo_id']

        queries = config.get_todo_queries()
        todo_item = queries.get_todo(self.todo_id)
        if todo_item:
            self.success_url = django.urls.reverse(
                'list', kwargs={'list_id': todo_item.list_id},
            )
        else:  # pragma: no cover
            self.success_url = django.urls.reverse('lists')

        return super().post(request, *args, **kwargs)

    def form_valid(self, form: NewListForm) -> http.HttpResponse:
        application = config.get_upvote_service()
        try:
            application.upvote(
                todo_id=self.todo_id,
                # See Note [User identification is naive]
                user_id=self.request.user.username,  # type: ignore[arg-type]
                upvote_at=datetime.datetime.now(datetime.UTC),
            )
        except todo_services.AlreadyUpvoted:  # pragma: no cover
            pass  # nothing to do
        except todo_services.TodoDoesNotExist:  # pragma: no cover
            messages.error(self.request, "That todo doesn't exist anymore 🤔")

        return super().form_valid(form)


class RemoveUpvoteFromTodo(LoginRequiredMixin, generic.FormView):  # type: ignore[type-arg]
    # TypeError: type 'FormView' is not subscriptable

    form_class = forms.Form

    def post(
            self, request: http.HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:
        self.todo_id = kwargs['todo_id']

        queries = config.get_todo_queries()
        todo_item = queries.get_todo(self.todo_id)
        if todo_item:
            self.success_url = django.urls.reverse(
                'list', kwargs={'list_id': todo_item.list_id},
            )
        else:  # pragma: no cover
            self.list_id = django.urls.reverse('lists')

        return super().post(request, *args, **kwargs)

    def form_valid(self, form: NewListForm) -> http.HttpResponse:
        application = config.get_upvote_service()
        try:
            application.remove_upvote(
                todo_id=self.todo_id,
                # See Note [User identification is naive]
                user_id=self.request.user.username,  # type: ignore[arg-type]
                remove_at=datetime.datetime.now(datetime.UTC),
            )
        except todo_services.NotUpvoted:  # pragma: no cover
            pass  # nothing to do
        except todo_services.TodoDoesNotExist:  # pragma: no cover
            messages.error(self.request, "That todo doesn't exist anymore 🤔")

        return super().form_valid(form)


class CompleteTodo(LoginRequiredMixin, generic.FormView):  # type: ignore[type-arg]
    # TypeError: type 'FormView' is not subscriptable

    form_class = forms.Form

    def post(
            self, request: http.HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:
        self.todo_id = kwargs['todo_id']
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: NewListForm) -> http.HttpResponse:
        application = config.get_complete_service()
        try:
            application.mark_done(
                todo_id=self.todo_id,
                # See Note [User identification is naive]
                user_id=self.request.user.username,  # type: ignore[arg-type]
                record_at=datetime.datetime.now(datetime.UTC),
            )
        except todo_services.AlreadyDone:  # pragma: no cover
            pass  # nothing to do
        except todo_services.TodoDoesNotExist:  # pragma: no cover
            messages.error(self.request, "That todo doesn't exist anymore 🤔")

        return super().form_valid(form)

    def get_success_url(self) -> str:
        queries = config.get_todo_queries()
        todo_item = queries.get_todo(self.todo_id)
        if todo_item:
            return django.urls.reverse(
                'list', kwargs={'list_id': todo_item.list_id},
            )
        else:  # pragma: no cover
            return django.urls.reverse('lists')

# Auth
# ====


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    password_confirm = forms.CharField()

    def clean_password_confirm(self) -> Any:
        # this is adapted from django.contrib.auth.forms.PasswordChangeForm
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "The two password fields didn't match.",
                code='password_mismatch',
            )

        password_validation.validate_password(password)  # type: ignore[arg-type]

        return password_confirm


class Signup(generic.FormView):  # type: ignore[type-arg]
    # TypeError: type 'FormView' is not subscriptable

    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = django.urls.reverse_lazy('lists')

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, *args: Any, **kwargs: Any) -> http.response.HttpResponseBase:
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form: SignupForm) -> http.HttpResponse:
        auth_models.User.objects.create_user(
            form.cleaned_data['username'], '', form.cleaned_data['password'],
        )

        return super().form_valid(form)
