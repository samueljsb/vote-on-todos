from __future__ import annotations

import abc
import datetime
import uuid
from collections.abc import Sequence
from typing import Protocol
from typing import TypeAlias

import attrs

UserId: TypeAlias = str
TodoId: TypeAlias = str
ListId: TypeAlias = str


# Events
# ======


@attrs.frozen
class Event(abc.ABC):
    timestamp: datetime.datetime
    todo_id: TodoId
    index: int


@attrs.frozen
class TodoCreatedV1(Event):
    list_id: ListId
    title: str
    description: str
    created_by: UserId


@attrs.frozen
class TodoUpvotedV1(Event):
    upvoted_by: UserId


@attrs.frozen
class TodoUpvoteRemovedV1(Event):
    removed_by: UserId


@attrs.frozen
class TodoDoneV1(Event):
    recorded_by: UserId


# Services
# ========


class ListQueries(Protocol):
    def is_list(self, list_id: ListId) -> bool: ...


class TodoQueries(Protocol):
    def get_todo(self, todo_id: TodoId) -> TodoItem | None: ...


@attrs.frozen
class ListDoesNotExist(Exception):
    list_id: ListId


@attrs.frozen
class NewTodo:
    lists: ListQueries

    def create_new_todo(
            self,
            title: str,
            *,
            description: str,
            list_id: ListId,
            created_by: str,
            created_at: datetime.datetime,
    ) -> TodoCreatedV1:
        if not self.lists.is_list(list_id):
            raise ListDoesNotExist(list_id)

        return TodoCreatedV1(
            timestamp=created_at,
            index=1,
            todo_id=uuid.uuid4().hex,
            list_id=list_id,
            title=title,
            description=description,
            created_by=created_by,
        )


class TodoDoesNotExist(Exception):
    pass


class AlreadyUpvoted(Exception):
    pass


class NotUpvoted(Exception):
    pass


@attrs.frozen
class Voting:
    todos: TodoQueries

    def upvote(
            self,
            todo_id: str,
            *,
            user_id: UserId,
            upvote_at: datetime.datetime,
    ) -> TodoUpvotedV1:
        todo = self.todos.get_todo(todo_id)

        if todo is None:
            raise TodoDoesNotExist
        elif user_id in todo.upvotes:
            raise AlreadyUpvoted

        return TodoUpvotedV1(
            timestamp=upvote_at,
            todo_id=todo_id,
            index=todo.next_index,
            upvoted_by=user_id,
        )

    def remove_upvote(
            self,
            todo_id: str,
            *,
            user_id: UserId,
            remove_at: datetime.datetime,
    ) -> TodoUpvoteRemovedV1:
        todo = self.todos.get_todo(todo_id)

        if todo is None:
            raise TodoDoesNotExist
        elif user_id not in todo.upvotes:
            raise NotUpvoted

        return TodoUpvoteRemovedV1(
            timestamp=remove_at,
            todo_id=todo_id,
            index=todo.next_index,
            removed_by=user_id,
        )


class AlreadyDone(Exception):
    pass


@attrs.frozen
class Completion:
    todos: TodoQueries

    def mark_done(
            self,
            todo_id: str,
            *,
            user_id: UserId,
            record_at: datetime.datetime,
    ) -> TodoDoneV1:
        todo = self.todos.get_todo(todo_id)

        if todo is None:
            raise TodoDoesNotExist
        elif todo.done_at is not None:
            raise AlreadyDone

        return TodoDoneV1(
            timestamp=record_at,
            todo_id=todo_id,
            index=todo.next_index,
            recorded_by=user_id,
        )

# Projections
# ===========


@attrs.define
class TodoItem:
    id: TodoId
    next_index: int

    list_id: ListId
    title: str
    description: str
    creator: UserId
    created_at: datetime.datetime
    done_at: datetime.datetime | None = None
    completor: UserId | None = None

    upvotes: set[UserId] = attrs.field(factory=set)


def get_items(events: Sequence[Event]) -> dict[TodoId, TodoItem]:
    items: dict[TodoId, TodoItem] = {}
    for event in events:
        if isinstance(event, TodoCreatedV1):
            items[event.todo_id] = TodoItem(
                id=event.todo_id,
                next_index=event.index + 1,
                list_id=event.list_id,
                title=event.title,
                description=event.description,
                creator=event.created_by,
                created_at=event.timestamp,
            )
        elif isinstance(event, TodoUpvotedV1):
            items[event.todo_id].upvotes.add(event.upvoted_by)
            items[event.todo_id].next_index = event.index + 1
        elif isinstance(event, TodoUpvoteRemovedV1):
            items[event.todo_id].upvotes.remove(event.removed_by)
            items[event.todo_id].next_index = event.index + 1
        elif isinstance(event, TodoDoneV1):
            items[event.todo_id].done_at = event.timestamp
            items[event.todo_id].completor = event.recorded_by
            items[event.todo_id].next_index = event.index + 1
        else:  # pragma: no cover
            raise TypeError(f'unexpected event type: {type(event)!r}')

    return items
