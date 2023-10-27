from __future__ import annotations

import datetime
import functools

import factory

from vote_on_todos.todos.domain import todos


# Factories
# =========


class Event(factory.Factory):
    class Meta:
        model = todos.Event
        abstract = True

    index = factory.Sequence(int)
    timestamp = factory.LazyFunction(
        functools.partial(datetime.datetime.now, datetime.UTC),
    )


class TodoCreatedV1(Event):
    class Meta:
        model = todos.TodoCreatedV1

    todo_id: str
    list_id: str

    title = 'Something I must do'
    description = 'A very important thing'
    created_by = 'me'
