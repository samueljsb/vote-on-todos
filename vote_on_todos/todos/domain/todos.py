from __future__ import annotations

import abc
import datetime
import uuid
from typing import Protocol
from typing import TypeAlias

import attrs

UserId: TypeAlias = str
TodoId: TypeAlias = str
ListId: TypeAlias = str


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


class ListQueries(Protocol):
    def is_list(self, list_id: ListId) -> bool: ...


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
