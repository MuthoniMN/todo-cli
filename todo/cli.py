from typing import Optional
import typer
from todo import (
        __app_name__,
        __version__,
        ERRORS,
        database,
        DB_WRITE_ERROR,
        DB_READ_ERROR,
        INITIALIZATION_ERROR
        )
from todo.todo import TodoController
from rich import print

app = typer.Typer()
todoController = TodoController()


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
def add():
    """
    Creates a new to-do for today.

    You'll be prompted for the following:\n
        1. title - name of the task\n
        2. category\n
        3. priority - high, medium, low
    """
    todo = TodoController()
    todo.title = typer.prompt("What task would you like to add?")
    todo.category = typer.prompt("What's the task's category?").lower()
    todo.priority = typer.prompt("What's the task's priority?").lower()
    try:
        todo.create_todo()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_WRITE_ERROR]}")
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


@app.command()
def find(task: str) -> None:
    """
    View a single task.
    """
    todo = TodoController()
    todo.title = task

    try:
        todo.find_todo()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_READ_ERROR]}")
        typer.Exit(1)
