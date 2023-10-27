from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import assert_never

from django.db import IntegrityError
from django.db import transaction

from . import models
from vote_on_todos.todos.application import unit_of_work
from vote_on_todos.todos.domain import lists
from vote_on_todos.todos.domain import todos


class DjangoCommitter:
    @contextmanager
    def atomic(self) -> Iterator[None]:
        with transaction.atomic():
            yield

    def handle(self, event: lists.Event | todos.Event) -> None:
        if isinstance(event, lists.Event):
            _new_list_event(event)
        elif isinstance(event, todos.Event):
            _new_todo_event(event)
        else:
            assert_never(event)


def _new_list_event(event: lists.Event) -> None:
    event_type, event_type_version = models.LIST_EVENT_TYPES[type(event)]
    new_event = models.ListEvent.objects.create(
        event_type=event_type,
        event_type_version=event_type_version,
        timestamp=event.timestamp,
        list_id=event.list_id,
        payload=models.ListEvent.payload_converter.dumps(event),
    )
    try:
        models.ListEventSequence.objects.create(
            event=new_event,
            list_id=event.list_id,
            index=event.index,
        )
    except IntegrityError as e:
        raise unit_of_work.StaleState from e


def _new_todo_event(event: todos.Event) -> None:
    event_type, event_type_version = models.TODO_EVENT_TYPES[type(event)]
    new_event = models.TodoEvent.objects.create(
        event_type=event_type,
        event_type_version=event_type_version,
        timestamp=event.timestamp,
        todo_id=event.todo_id,
        payload=models.TodoEvent.payload_converter.dumps(event),
    )
    try:
        models.TodoEventSequence.objects.create(
            event=new_event,
            todo_id=event.todo_id,
            index=event.index,
        )
    except IntegrityError as e:
        raise unit_of_work.StaleState from e
