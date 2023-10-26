from __future__ import annotations

import datetime

import attrs

from . import unit_of_work
from vote_on_todos.todos.domain import todos


class ListDoesNotExist(Exception):
    pass


@attrs.frozen
class NewTodo:
    committer: unit_of_work.Committer
    lists: todos.ListQueries

    def create_new_todo(
        self,
        title: str,
        *,
        list_id: str,
        description: str,
        created_by: str,
        created_at: datetime.datetime,
    ) -> None:
        """Create a new todo item.

        Raises:
            ListDoesNotExist: The list does not exist.
        """
        with unit_of_work.commit_on_success(self.committer) as new_events:
            domain = todos.NewTodo(lists=self.lists)

            try:
                new_event = domain.create_new_todo(
                    title,
                    description=description,
                    list_id=list_id,
                    created_by=created_by,
                    created_at=created_at,
                )
            except todos.ListDoesNotExist as e:
                raise ListDoesNotExist from e
            else:
                new_events.append(new_event)
