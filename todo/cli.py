from typing import Optional
import typer
from todo import (
        __app_name__,
        __version__,
        ERRORS,
        database,
        INITIALIZATION_ERROR,
        DB_READ_ERROR,
        todos,
        tasks
        )
from todo.todo import TodoController
from rich import print

app = typer.Typer()
app.add_typer(todos.app, name="todos")
app.add_typer(tasks.app, name="tasks")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version",
        callback=_version_callback,
        is_eager=True
    )
) -> None:
    return


@app.command()
def init():
    """
    Initialize application.

    Connecting to the database and creating the necessary tables
    """
    try:
        database.create_tables()
        typer.echo("App initialized successfully!")
    except Exception as e:
        typer.echo(e)
        typer.echo("Error: {ERRORS[INITIALIZATION_ERROR]}")
        typer.Exit(1)


@app.command()
def drop():
    """
    Drop the existing tables.
    """
    try:
        database.drop_tables()
        typer.echo("Database tables dropped.")
    except Exception as e:
        print(e)
        typer.echo("Error: Failed to drop tables")
        typer.Exit(1)


@app.command()
def list() -> None:
    """
    Get your to-do list for today.

    Returns all the tasks created for today
    """
    todo = TodoController()
    try:
        todo.list_todos()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_READ_ERROR]}")
        typer.Exit(1)
