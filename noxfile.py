from __future__ import annotations

import nox

nox.options.sessions = ['pip_compile', 'makemigrations', 'test', 'lint']


_LOCAL_SETTINGS_MODULE = 'vote_on_todos.website.settings.local'


@nox.session(python='3.12', reuse_venv=True)
def test(session: nox.Session) -> None:
    """Run tests."""
    session.install(
        '-r', 'requirements/prod.txt',
        '-r', 'requirements/test.txt',
    )
    session.run('coverage', 'erase')
    session.run(
        'coverage', 'run', '-m', 'pytest', 'tests', *session.posargs,
    )
    session.run('coverage', 'report')


@nox.session(python='3.12', reuse_venv=True)
def lint(session: nox.Session) -> None:
    """Run linters."""
    session.install('pre-commit')
    session.run('pre-commit', 'run', '--all-files')


def _pip_compile(session: nox.Session, path: str) -> None:
    session.run(
        'pip-compile', path,
        env={'CUSTOM_COMPILE_COMMAND': 'nox -s pip_compile'},
    )


@nox.session(python='3.12')
def pip_compile(session: nox.Session) -> None:
    """Compile dependency files."""
    session.install('pip-tools')
    with session.chdir('requirements/'):
        _pip_compile(session, 'prod.in')
        _pip_compile(session, 'test.in')


@nox.session(python='3.12')
def pip_audit(session: nox.Session) -> None:
    """Audit dependencies for known vulnerabilities.

    Will fix those problems if it can.
    """
    session.install('pip-audit')
    session.run(
        'pip-audit', '--desc',
        '-r', 'requirements/prod.txt',
        '-r', 'requirements/test.txt',
        '--fix',
    )

    # if there are changes, re-compile dependencies
    try:
        session.run('git', 'diff', '--quiet')
    except nox.command.CommandFailed:
        session.notify('pip_compile')


@nox.session(python='3.12')
def makemigrations(session: nox.Session) -> None:
    """Make Django migrations."""
    session.install('-r', 'requirements/prod.txt')
    session.run(
        'python', '-m', 'manage', 'makemigrations',
        env={'DJANGO_SETTINGS_MODULE': _LOCAL_SETTINGS_MODULE},
    )


@nox.session(python='3.12', reuse_venv=True)
def runserver(session: nox.Session) -> None:
    """Run the Django server."""
    session.install('-r', 'requirements/prod.txt')

    session.run(
        'python', '-m', 'manage', 'migrate',
        env={'DJANGO_SETTINGS_MODULE': _LOCAL_SETTINGS_MODULE},
    )
    session.run(
        'python', '-m', 'manage', 'runserver', *session.posargs,
        env={'DJANGO_SETTINGS_MODULE': _LOCAL_SETTINGS_MODULE},
    )
