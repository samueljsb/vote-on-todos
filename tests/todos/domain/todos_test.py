from __future__ import annotations

import datetime
from unittest import mock

import pytest

from testing import lists as list_helpers
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
