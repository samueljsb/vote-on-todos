from __future__ import annotations

import datetime
from unittest import mock

from testing.unit_of_work import Committer
from vote_on_todos.todos.application import lists
from vote_on_todos.todos.domain import lists as domain


class TestNewList:
    def test_create_new_list(self):
        committer = Committer()
        use_case = lists.NewList(committer=committer)

        use_case.create_new_list(
            'My List',
            description='Things I need to do',
            created_by='user-1',
            created_at=datetime.datetime(2023, 1, 2, 3, 4, 5),
        )

        assert committer.committed == [
            domain.ListCreatedV1(
                timestamp=datetime.datetime(2023, 1, 2, 3, 4, 5),
                index=1,
                list_id=mock.ANY,
                name='My List',
                description='Things I need to do',
                created_by='user-1',
            ),
        ]
