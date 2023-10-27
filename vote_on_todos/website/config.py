from __future__ import annotations

from vote_on_todos.django_back_end import queries
from vote_on_todos.django_back_end import unit_of_work
from vote_on_todos.todos.application.lists import NewList


def get_committer() -> unit_of_work.DjangoCommitter:
    return unit_of_work.DjangoCommitter()


def get_list_queries() -> queries.ListRepo:
    return queries.ListRepo()


def get_new_list_service() -> NewList:
    return NewList(committer=get_committer())
