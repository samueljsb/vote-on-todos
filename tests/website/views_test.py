from __future__ import annotations

import pytest
from django_webtest import DjangoTestApp

pytestmark = pytest.mark.django_db(transaction=True)


def test_lists_none_found(django_app: DjangoTestApp):
    response = django_app.get('/lists/')

    assert response.status_code == 200
    assert 'no lists: you should create one!' in response

# TODO: test with lists
