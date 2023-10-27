from __future__ import annotations

from . import models
from vote_on_todos.todos.domain import lists


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

    def is_list(self, list_id: str) -> bool:
        return list_id in self._get_lists(list_id)
