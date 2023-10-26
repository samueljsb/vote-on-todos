from __future__ import annotations

import datetime

import attrs

from . import unit_of_work
from vote_on_todos.todos.domain import lists


@attrs.frozen
class NewList:
    committer: unit_of_work.Committer

    def create_new_list(
        self,
        name: str,
        *,
        description: str,
        created_by: str,
        created_at: datetime.datetime,
    ) -> None:
        """Create a new list of todos."""
        with unit_of_work.commit_on_success(self.committer) as new_events:
            domain = lists.NewList()
            new_event = domain.create_new_list(
                name,
                description=description,
                created_by=created_by,
                created_at=created_at,
            )
            new_events.append(new_event)
