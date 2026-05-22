from __future__ import annotations

import json

import click

from .client import get_context, list_owners, summary


def emit(payload: object) -> None:
    click.echo(json.dumps(payload, indent=2, sort_keys=True))


@click.group()
def main() -> None:
    """Saia-Nitroy household context tool."""


@main.command()
def context() -> None:
    """Show household deployment context."""
    emit(get_context())


@main.command()
def owners() -> None:
    """List household owners."""
    emit({"owners": list_owners()})


@main.command()
def brief() -> None:
    """Summarize household deployment context."""
    emit(summary())


if __name__ == "__main__":
    main()
