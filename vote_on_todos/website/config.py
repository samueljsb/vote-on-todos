from __future__ import annotations

from vote_on_todos.django_back_end import queries


def get_list_queries() -> queries.ListRepo:
    return queries.ListRepo()
