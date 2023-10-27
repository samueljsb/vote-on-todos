from __future__ import annotations

import cattrs.preconf.json
from django.db import models

from vote_on_todos.todos.domain import lists
from vote_on_todos.todos.domain import todos


# Lists
# =====

LIST_EVENT_TYPES: dict[type[lists.Event], tuple[str, int]] = {
    lists.ListCreatedV1: ('ListCreated', 1),
}


def list_event_type(event_type: str, version: int) -> type[lists.Event]:
    return {v: k for k, v in LIST_EVENT_TYPES.items()}[(event_type, version)]


class ListEvent(models.Model):
    event_type = models.CharField(max_length=100)
    event_type_version = models.IntegerField()

    list_id = models.CharField(max_length=100, db_index=True)

    timestamp = models.DateTimeField()
    payload = models.CharField(max_length=500)
    payload_converter = cattrs.preconf.json.make_converter()


class ListEventSequence(models.Model):
    event = models.ForeignKey(ListEvent, on_delete=models.PROTECT)
    list_id = models.CharField(max_length=100)
    index = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['list_id', 'index'], name='unique_index_per_list_id',
            ),
        ]


# Todos
# =====
TODO_EVENT_TYPES: dict[type[todos.Event], tuple[str, int]] = {
    todos.TodoCreatedV1: ('TodoCreated', 1),
    todos.TodoUpvotedV1: ('TodoUpvoted', 1),
}


def todo_event_type(event_type: str, version: int) -> type[todos.Event]:
    return {v: k for k, v in TODO_EVENT_TYPES.items()}[(event_type, version)]


class TodoEvent(models.Model):
    event_type = models.CharField(max_length=100)
    event_type_version = models.IntegerField()

    todo_id = models.CharField(max_length=100, db_index=True)

    timestamp = models.DateTimeField()
    payload = models.CharField(max_length=500)
    payload_converter = cattrs.preconf.json.make_converter()


class TodoEventSequence(models.Model):
    event = models.ForeignKey(TodoEvent, on_delete=models.PROTECT)
    todo_id = models.CharField(max_length=100)
    index = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['todo_id', 'index'], name='unique_index_per_todo_id',
            ),
        ]
