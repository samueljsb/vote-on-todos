from __future__ import annotations

import datetime
from unittest import mock

import pytest

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
