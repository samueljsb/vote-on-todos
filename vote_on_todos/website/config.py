from __future__ import annotations

from vote_on_todos.django_back_end import queries
from vote_on_todos.django_back_end import unit_of_work
from vote_on_todos.todos.application.lists import NewList
from vote_on_todos.todos.application.todos import NewTodo


def get_committer() -> unit_of_work.DjangoCommitter:
    return unit_of_work.DjangoCommitter()


def get_list_queries() -> queries.ListRepo:
    return queries.ListRepo()


def get_todo_queries() -> queries.TodoRepo:
    return queries.TodoRepo()


def get_new_list_service() -> NewList:
    return NewList(committer=get_committer())


def get_new_todo_service() -> NewTodo:
    return NewTodo(
        lists=get_list_queries(),
        committer=get_committer(),
    )
