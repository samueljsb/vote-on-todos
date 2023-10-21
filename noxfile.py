from __future__ import annotations

import nox


@nox.session(python="3.12", reuse_venv=True)
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


def _pip_compile(session: nox.Session, path: str) -> None:
    session.run(
        'pip-compile', path,
        env={'CUSTOM_COMPILE_COMMAND': 'nox -s pip_compile'},
    )


@nox.session
def pip_compile(session: nox.Session) -> None:
    """Compile dependency files."""
    session.install('pip-tools')
    _pip_compile(session, 'requirements/prod.in')
    _pip_compile(session, 'requirements/test.in')
