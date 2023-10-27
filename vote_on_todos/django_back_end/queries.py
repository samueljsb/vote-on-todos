from __future__ import annotations

from collections import defaultdict

from . import models
from vote_on_todos.todos.domain import lists
from vote_on_todos.todos.domain import todos


class ListRepo:
    def _get_lists(self, list_id: str | None = None) -> dict[str, lists.TodoList]:
        qs = models.ListEvent.objects.all()

        if list_id is not None:
            qs = qs.filter(list_id=list_id)

        events = [
            models.ListEvent.payload_converter.loads(
                evt.payload, models.list_event_type(
                    evt.event_type, evt.event_type_version,
                ),
            )
            for evt in qs.order_by('timestamp')
        ]

        return lists.get_lists(events)

    def get_lists(self) -> list[lists.TodoList]:
        return list(self._get_lists().values())

    def get_list(self, list_id: str) -> lists.TodoList:
        return self._get_lists()[list_id]

    def is_list(self, list_id: str) -> bool:
        return list_id in self._get_lists(list_id)


class TodoRepo:
    def _get_lists(self) -> dict[str, list[todos.TodoItem]]:
        qs = models.TodoEvent.objects.all()

        events = [
            models.TodoEvent.payload_converter.loads(
                evt.payload, models.todo_event_type(
                    evt.event_type, evt.event_type_version,
                ),
            )
            for evt in qs.order_by('timestamp')
        ]

        todo_items = todos.get_items(events)

        todo_lists = defaultdict(list)
        for item in todo_items.values():
            todo_lists[item.list_id].append(item)

        return todo_lists

    def get_list(self, list_id: str) -> list[todos.TodoItem]:
        return self._get_lists()[list_id]
