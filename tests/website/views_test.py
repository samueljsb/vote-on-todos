from __future__ import annotations

import pytest
from django_webtest import DjangoTestApp
from django_webtest import DjangoWebtestResponse

pytestmark = pytest.mark.django_db(transaction=True)


def _create_list(
    django_app: DjangoTestApp, name: str, description: str,
) -> DjangoWebtestResponse:
    page = django_app.get('/new-list/')
    form = page.form
    form['list_name'] = name
    form['description'] = description
    return form.submit()


def test_lists(django_app: DjangoTestApp):
    _create_list(django_app, 'My List', 'Things I need to do')

    response = django_app.get('/lists/')

    assert response.status_code == 200
    assert 'My List' in response
    assert 'no lists' not in response


def test_lists_none_found(django_app: DjangoTestApp):
    response = django_app.get('/lists/')

    assert response.status_code == 200
    assert 'no lists: you should create one!' in response


def test_create_new_list(django_app: DjangoTestApp):
    response = _create_list(django_app, 'My List', 'Things I need to do')

    assert response.status_code == 302

    response = response.follow()
    assert response.status_code == 200

    # TODO: assertions on the content of the response
