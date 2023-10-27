from __future__ import annotations

import datetime
import functools
from collections.abc import Collection

import attrs
import factory

from vote_on_todos.todos.domain import lists


@attrs.frozen
class ListRepo:
    list_ids: Collection[str] = ()

    def is_list(self, list_id: str) -> bool:
        return list_id in self.list_ids


# Factories
# =========


class Event(factory.Factory):
    class Meta:
        model = lists.Event
        abstract = True

    index = factory.Sequence(int)
    timestamp = factory.LazyFunction(
        functools.partial(datetime.datetime.now, datetime.UTC),
    )


class ListCreatedV1(Event):
    class Meta:
        model = lists.ListCreatedV1

    list_id: str

    name = 'My List'
    description = 'Things I need to do'
    created_by = 'me'
