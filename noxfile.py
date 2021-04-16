"""Nox sessions."""

import nox
from nox.sessions import Session

package = "orm_async_tests"

# Default locations
locations = ("src", "noxfile.py")
# List of sessions that run if nox is called without specifying session.
nox.options.sessions = ("lint",)


@nox.session(python=False)
def fmt(session: Session) -> None:
    """Formats code-"""
    args = session.posargs or locations
    session.run("isort", "--force-single-line-imports", *args)
    session.run(
        "autoflake",
        "--remove-all-unused-imports",
        "--recursive",
        "--remove-unused-variables",
        "--in-place",
        *args,
    )
    session.run("black", *args)
    session.run("isort", *args)


@nox.session(python=False)
def lint(session: Session) -> None:
    """Check code quality with flake8, black, isort, mypy and all the installed plugins."""
    args = session.posargs or locations
    session.run("flake8", *args)
    session.run("black", "--check", *args)
    session.run("isort", "--check-only", *args)
    session.run("mypy", *args)

