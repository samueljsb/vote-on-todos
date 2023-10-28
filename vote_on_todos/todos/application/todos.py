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


class TodoDoesNotExist(Exception):
    pass


class AlreadyUpvoted(Exception):
    pass


class NotUpvoted(Exception):
    pass


@attrs.frozen
class Upvote:
    committer: unit_of_work.Committer
    _todos: todos.TodoQueries

    def upvote(
        self, *,
        todo_id: str, user_id: str,
        upvote_at: datetime.datetime,
    ) -> None:
        """Upvote a todo item.

        Raises:
            TodoDoesNotExist: The todo item does not exist.
            AlreadyUpvoted: This todo item has already been upvoted by this user.
        """
        with unit_of_work.commit_on_success(self.committer) as new_events:
            domain = todos.Voting(todos=self._todos)

            try:
                new_event = domain.upvote(
                    todo_id,
                    user_id=user_id,
                    upvote_at=upvote_at,
                )
            except todos.TodoDoesNotExist as e:
                raise TodoDoesNotExist from e
            except todos.AlreadyUpvoted as e:
                raise AlreadyUpvoted from e
            else:
                new_events.append(new_event)

    def remove_upvote(
        self, *,
        todo_id: str, user_id: str,
        remove_at: datetime.datetime,
    ) -> None:
        """Upvote a todo item.

        Raises:
            TodoDoesNotExist: The todo item does not exist.
            NotUpvoted: This todo item has not been upvoted by this user.
        """
        with unit_of_work.commit_on_success(self.committer) as new_events:
            domain = todos.Voting(todos=self._todos)

            try:
                new_event = domain.remove_upvote(
                    todo_id,
                    user_id=user_id,
                    remove_at=remove_at,
                )
            except todos.TodoDoesNotExist as e:
                raise TodoDoesNotExist from e
            except todos.NotUpvoted as e:
                raise NotUpvoted from e
            else:
                new_events.append(new_event)
