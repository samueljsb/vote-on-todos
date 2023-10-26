from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import attrs

from vote_on_todos.todos.domain import lists
from vote_on_todos.todos.domain import todos


@attrs.define
class Committer:
    """A fake committer for use in tests."""
    committed: list[lists.Event | todos.Event] = attrs.field(
        init=False, factory=list,
    )
    uncommitted_events: list[
        lists.Event |
        todos.Event
    ] = attrs.field(init=False)

    @contextmanager
    def atomic(self) -> Iterator[None]:
        self.uncommitted_events: list[lists.Event | todos.Event] = []
        yield
        self.committed.extend(self.uncommitted_events)
        del self.uncommitted_events

    def handle(self, event: lists.Event | todos.Event) -> None:
        self.uncommitted_events.append(event)
