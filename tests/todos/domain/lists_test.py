from __future__ import annotations

import datetime
from unittest import mock

from vote_on_todos.todos.domain import lists


class TestNewList:
    def test_new_list(self):
        new_list = lists.NewList()

        event = new_list.create_new_list(
            'My List',
            description='A list of nice things',
            created_by='user-1',
            created_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert event == lists.ListCreatedV1(
            timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
            index=1,
            list_id=mock.ANY,
            name='My List',
            description='A list of nice things',
            created_by='user-1',
        )
