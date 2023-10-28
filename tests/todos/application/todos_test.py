from __future__ import annotations

import datetime
from unittest import mock

import pytest

from testing import todos as todo_helpers
from testing.lists import ListRepo
from testing.unit_of_work import Committer
from vote_on_todos.todos.application import todos
from vote_on_todos.todos.domain import todos as domain


class TestNewList:
    def test_create_new_todo(self):
        committer = Committer()
        use_case = todos.NewTodo(
            committer=committer,
            lists=ListRepo({'list-1'}),
        )

        use_case.create_new_todo(
            'Do something',
            description='There are a lot of steps to this one...',
            list_id='list-1',
            created_by='user-1',
            created_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert committer.committed == [
            domain.TodoCreatedV1(
                timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
                index=1,
                todo_id=mock.ANY,
                list_id='list-1',
                title='Do something',
                description='There are a lot of steps to this one...',
                created_by='user-1',
            ),
        ]

    def test_create_new_todo_on_nonexistent_list(self):
        committer = Committer()
        use_case = todos.NewTodo(
            committer=committer,
            lists=ListRepo({'list-1'}),
        )

        with pytest.raises(todos.ListDoesNotExist):
            use_case.create_new_todo(
                'Do something',
                description='There are a lot of steps to this one...',
                list_id='list-5',  # does not exist
                created_by='user-1',
                created_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

        assert committer.committed == []


class TestUpvote:
    def test_upvote(self):
        committer = Committer()
        use_case = todos.Upvote(
            committer=committer,
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(id='todo-1', next_index=2),
            }),
        )

        use_case.upvote(
            todo_id='todo-1', user_id='some-user',
            upvote_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert committer.committed == [
            domain.TodoUpvotedV1(
                timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
                index=2,
                todo_id='todo-1',
                upvoted_by='some-user',
            ),
        ]

    def test_upvote_nonexistent_todo(self):
        committer = Committer()
        use_case = todos.Upvote(
            committer=committer,
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(id='todo-1', next_index=2),
            }),
        )

        with pytest.raises(todos.TodoDoesNotExist):
            use_case.upvote(
                todo_id='todo-2', user_id='some-user',
                upvote_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

        assert committer.committed == []

    def test_upvote_already_upvoted(self):
        committer = Committer()
        use_case = todos.Upvote(
            committer=committer,
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(
                    id='todo-1', next_index=2, upvotes={'some-user'},
                ),
            }),
        )

        with pytest.raises(todos.AlreadyUpvoted):
            use_case.upvote(
                todo_id='todo-1', user_id='some-user',
                upvote_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

        assert committer.committed == []

    def test_remove_upvote(self):
        committer = Committer()
        use_case = todos.Upvote(
            committer=committer,
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(
                    id='todo-1', next_index=2, upvotes={'some-user'},
                ),
            }),
        )

        use_case.remove_upvote(
            todo_id='todo-1', user_id='some-user',
            remove_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert committer.committed == [
            domain.TodoUpvoteRemovedV1(
                timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
                index=2,
                todo_id='todo-1',
                removed_by='some-user',
            ),
        ]

    def test_remove_upvote_from_nonexistent_todo(self):
        committer = Committer()
        use_case = todos.Upvote(
            committer=committer,
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(id='todo-1', next_index=2),
            }),
        )

        with pytest.raises(todos.TodoDoesNotExist):
            use_case.remove_upvote(
                todo_id='todo-2', user_id='some-user',
                remove_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

        assert committer.committed == []

    def test_remove_upvote_from_todo_not_upvoted(self):
        committer = Committer()
        use_case = todos.Upvote(
            committer=committer,
            todos=todo_helpers.TodoRepo({
                'todo-1': todo_helpers.TodoItem(
                    id='todo-1', next_index=2, upvotes={},
                ),
            }),
        )

        with pytest.raises(todos.NotUpvoted):
            use_case.remove_upvote(
                todo_id='todo-1', user_id='some-user',
                remove_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
            )

        assert committer.committed == []
