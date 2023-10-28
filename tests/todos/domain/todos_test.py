from __future__ import annotations

import datetime
from unittest import mock

import pytest

from testing import lists as list_helpers
from testing import todos as todo_helpers
from vote_on_todos.todos.domain import todos


class TestNewList:
    def test_new_todo(self):
        new_todo = todos.NewTodo(
            lists=list_helpers.ListRepo({'list-1'}),
        )

        event = new_todo.create_new_todo(
            'Do something important',
            description="It's really very urgent",
            list_id='list-1',
            created_by='user-1',
            created_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert event == todos.TodoCreatedV1(
            timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
            index=1,
            todo_id=mock.ANY,
            list_id='list-1',
            title='Do something important',
            description="It's really very urgent",
            created_by='user-1',
        )

    def test_new_todo_on_nonexistent_list(self):
        new_todo = todos.NewTodo(
            lists=list_helpers.ListRepo({'list-1'}),
        )

        with pytest.raises(todos.ListDoesNotExist):
            new_todo.create_new_todo(
                'Do something important',
                description="It's really very urgent",
                list_id='list-5',
                created_by='user-1',
                created_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )


class TestVoting:
    def test_upvote_todo(self):
        voting = todos.Voting(
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(id='todo-1', next_index=2),
            }),
        )

        event = voting.upvote(
            'todo-1',
            user_id='someone',
            upvote_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert event == todos.TodoUpvotedV1(
            timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
            todo_id='todo-1',
            index=2, upvoted_by='someone',
        )

    def test_upvote_nonexistent_todo(self):
        voting = todos.Voting(
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(id='todo-1', next_index=2),
            }),
        )

        with pytest.raises(todos.TodoDoesNotExist):
            voting.upvote(
                'todo-2',
                user_id='someone',
                upvote_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

    def test_upvote_todo_already_upvoted(self):
        voting = todos.Voting(
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(
                    id='todo-1', next_index=3, upvotes={'someone'},
                ),
            }),
        )

        with pytest.raises(todos.AlreadyUpvoted):
            voting.upvote(
                'todo-1',
                user_id='someone',
                upvote_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

    def test_remove_upvote(self):
        voting = todos.Voting(
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(
                    id='todo-1', next_index=2, upvotes={'someone'},
                ),
            }),
        )

        event = voting.remove_upvote(
            'todo-1',
            user_id='someone',
            remove_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert event == todos.TodoUpvoteRemovedV1(
            timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
            todo_id='todo-1',
            index=2, removed_by='someone',
        )

    def test_remove_upvote_from_nonexistent_todo(self):
        voting = todos.Voting(
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(id='todo-1', next_index=2),
            }),
        )

        with pytest.raises(todos.TodoDoesNotExist):
            voting.remove_upvote(
                'todo-2',
                user_id='someone',
                remove_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

    def test_remove_upvote_from_todo_not_upvoted(self):
        voting = todos.Voting(
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(
                    id='todo-1', next_index=3, upvotes={},
                ),
            }),
        )

        with pytest.raises(todos.NotUpvoted):
            voting.remove_upvote(
                'todo-1',
                user_id='someone',
                remove_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )
