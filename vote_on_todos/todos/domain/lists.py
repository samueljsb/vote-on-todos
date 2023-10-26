from __future__ import annotations

import abc
import datetime
import uuid
from typing import TypeAlias

import attrs

UserId: TypeAlias = str
ListId: TypeAlias = str


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
