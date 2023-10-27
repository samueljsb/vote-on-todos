from __future__ import annotations

import pytest
from django_webtest import DjangoTestApp
from django_webtest import DjangoWebtestResponse

from vote_on_todos.django_back_end import queries

pytestmark = pytest.mark.django_db(transaction=True)


def _create_list(
    django_app: DjangoTestApp, name: str, description: str,
) -> DjangoWebtestResponse:
    page = django_app.get('/new-list/', user='some-user')
    form = page.form
    form['list_name'] = name
    form['description'] = description
    return form.submit()


def _create_todo(
    django_app: DjangoTestApp, list_id: str, title: str, description: str,
) -> DjangoWebtestResponse:
    page = django_app.get(f'/new-todo/{list_id}/', user='some-user')
    form = page.form
    form['title'] = title
    form['description'] = description
    return form.submit()


def test_redirected_to_login_if_not_logged_in(django_app: DjangoTestApp):
    response = django_app.get('/lists/')

    assert response.status_code == 302
    assert response.location == '/accounts/login/?next=/lists/'


def test_lists(django_app: DjangoTestApp):
    _create_list(django_app, 'My List', 'Things I need to do')

    response = django_app.get('/lists/', user='some-user')

    assert response.status_code == 200
    assert 'My List' in response
    assert 'no lists' not in response


def test_lists_none_found(django_app: DjangoTestApp):
    response = django_app.get('/lists/', user='some-user')

    assert response.status_code == 200
    assert 'no lists: you should create one!' in response


def test_create_new_list(django_app: DjangoTestApp):
    response = _create_list(django_app, 'My List', 'Things I need to do')

    assert response.status_code == 302

    response = response.follow()
    assert response.status_code == 200

    # TODO: assertions on the content of the response


def test_view_list_no_todos(django_app: DjangoTestApp):
    response = _create_list(django_app, 'My List', 'Things I need to do')

    list_id = queries.ListRepo().get_lists().pop().id

    response = django_app.get(f'/lists/{list_id}/', user='some-user')

    assert response.status_code == 200
    assert 'My List' in response
    assert 'no items yet: you should create one!' in response


def test_view_nonexistent_list(django_app: DjangoTestApp):
    django_app.get('/list/not-a-list/', user='some-user', status=404)


def test_create_new_todo(django_app: DjangoTestApp):
    _create_list(django_app, 'My List', 'Things I need to do')
    list_id = queries.ListRepo().get_lists().pop().id

    response = _create_todo(
        django_app, list_id,
        'Important task', 'This must be done soon!',
    )

    assert response.status_code == 302

    response = response.follow()
    assert response.status_code == 200

    # TODO: assertions on the content of the response
