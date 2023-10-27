from __future__ import annotations

import abc
import datetime
import uuid
from collections.abc import Sequence
from typing import TypeAlias

import attrs

UserId: TypeAlias = str
ListId: TypeAlias = str


# Events
# ======

@attrs.frozen
class Event(abc.ABC):
    timestamp: datetime.datetime
    list_id: ListId
    index: int


@attrs.frozen
class ListCreatedV1(Event):
    name: str
    description: str
    created_by: UserId


@attrs.frozen
class NewList:
    def create_new_list(
            self,
            name: str,
            *,
            description: str,
            created_by: UserId,
            created_at: datetime.datetime,
    ) -> ListCreatedV1:
        return ListCreatedV1(
            timestamp=created_at,
            index=1,
            list_id=uuid.uuid4().hex,
            name=name,
            description=description,
            created_by=created_by,
        )


# Projections
# ===========

@attrs.frozen
class TodoList:
    id: ListId
    name: str
    description: str
    creator: UserId


def get_lists(events: Sequence[Event]) -> dict[ListId, TodoList]:
    lists = {}
    for event in events:
        if isinstance(event, ListCreatedV1):
            lists[event.list_id] = TodoList(
                id=event.list_id,
                name=event.name,
                description=event.description,
                creator=event.created_by,
            )
        else:  # pragma: no cover
            raise TypeError(f"unexpected event type: {type(event)!r}")

    return lists
