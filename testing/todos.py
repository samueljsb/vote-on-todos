from __future__ import annotations

import datetime
import functools

import attrs
import factory

from vote_on_todos.todos.domain import todos


@attrs.frozen
class TodoRepo:
    _todos: dict[str, todos.TodoItem] = attrs.field(factory=dict)

    def get_todo(self, todo_id: str) -> todos.TodoItem | None:
        return self._todos.get(todo_id)


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


class TodoUpvotedV1(Event):
    class Meta:
        model = todos.TodoUpvotedV1

    todo_id: str
    upvoted_by = 'me'


class TodoItem(factory.Factory):
    class Meta:
        model = todos.TodoItem

    id: str
    next_index: int

    list_id = 'list-1'
    title = 'Something I must do'
    description = 'A very important thing'
    creator = 'me'
    created_at = factory.LazyFunction(datetime.datetime.now)

    upvotes = factory.LazyFunction(set)
