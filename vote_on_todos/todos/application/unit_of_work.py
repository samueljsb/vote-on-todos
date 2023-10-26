from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Protocol

from vote_on_todos.todos.domain import lists
from vote_on_todos.todos.domain import todos


@contextmanager
def commit_on_success(
        committer: Committer,
) -> Iterator[list[lists.Event | todos.Event]]:
    new_events: list[lists.Event | todos.Event] = []
    yield new_events
    with committer.atomic():
        for event in new_events:
            committer.handle(event)


class StaleState(Exception):
    """An event could not be handled because the state has changed."""


class Committer(Protocol):
    @contextmanager
    def atomic(self) -> Iterator[None]:
        """Apply handled events atomically.

        Raises:
            StaleState: The state has changed and committing is no longer safe.
        """
        ...

    def handle(self, event: lists.Event | todos.Event) -> None:
        """Handle a new event.

        Raises:
            StaleState: The state has changed and handling is no longer safe.
        """
        ...
