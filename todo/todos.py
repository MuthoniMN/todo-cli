import typer
from todo import (
        ERRORS,
        DB_WRITE_ERROR,
        DB_READ_ERROR,
        )
from todo.todo import TodoController
from rich import print

app = typer.Typer()


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

@app.command()
def complete(task: str) -> None:
    """
    Complete a task
    """
    todo = TodoController()
    todo.title = task

    try:
        todo.complete_todo()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_WRITE_ERROR]}")
        typer.Exit(1)


@app.command()
def delete(task: str) -> None:
    """
    Delete a task
    """
    todo = TodoController()
    todo.title = task
    try:
        todo.delete_todo()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_WRITE_ERROR]}")
        typer.Exit(1)
