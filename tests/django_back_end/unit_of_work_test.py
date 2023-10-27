from __future__ import annotations

import pytest

from testing import lists as list_helpers
from testing import todos as todo_helpers
from vote_on_todos.django_back_end.unit_of_work import DjangoCommitter
from vote_on_todos.todos.application import unit_of_work

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.parametrize(
    'indices',
    (
        pytest.param((1, 1), id='duplicate'),
        pytest.param((2, 1), id='out-of-order'),
    ),
)
def test_non_monotonic_list_event_insert_raises_StaleState(indices):
    committer = DjangoCommitter()

    # create a list
    committer.handle(
        list_helpers.ListCreatedV1(list_id='list-1', index=0),
    )

    # two processes attempt to insert an event for the same list...
    # TODO: use realistic events when we have more than one type
    # ... the first succeeds
    committer.handle(
        list_helpers.ListCreatedV1(list_id='list-1', index=indices[0]),
    )

    # ... the second fails
    with pytest.raises(unit_of_work.StaleState):
        committer.handle(
            list_helpers.ListCreatedV1(list_id='list-1', index=indices[1]),
        )


@pytest.mark.parametrize(
    'indices',
    (
        pytest.param((1, 1), id='duplicate'),
        pytest.param((2, 1), id='out-of-order'),
    ),
)
def test_non_monotonic_todo_event_insert_raises_StaleState(indices):
    committer = DjangoCommitter()

    # create a list
    committer.handle(
        todo_helpers.TodoCreatedV1(
            todo_id='todo-1', list_id='list-1', index=0,
        ),
    )

    # two processes attempt to insert an event for the same list...
    # TODO: use realistic events when we have more than one type
    # ... the first succeeds
    committer.handle(
        todo_helpers.TodoCreatedV1(
            todo_id='todo-1', list_id='list-1', index=indices[0],
        ),
    )

    # ... the second fails
    with pytest.raises(unit_of_work.StaleState):
        committer.handle(
            todo_helpers.TodoCreatedV1(
                todo_id='todo-1', list_id='list-1', index=indices[1],
            ),
        )
