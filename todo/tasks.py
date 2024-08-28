import typer
from todo import (
        ERRORS,
        DB_WRITE_ERROR,
        DB_READ_ERROR,
        )
from todo.task import TaskController
from rich import print
from datetime import datetime

app = typer.Typer()


@app.command()
def add():
    """
    Creates a new task.

    You'll be prompted for the following:\n
        1. title - name of the task\n
        2. category\n
        3. due date\n
        4. priority - high, medium, low
    """
    task = TaskController()
    task.title = typer.prompt("What task would you like to add?")
    task.category = typer.prompt("What's the task's category?").lower()
    task.priority = typer.prompt("What's the task's priority?").lower()
    datestr = typer.prompt("When is the task due?[FORMAT: DD/MM/YYYY]")
    day, month, year = datestr.split('/')
    task.date = datetime(int(year), int(month), int(day))
    print(task)
    try:
        task.create_task()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_WRITE_ERROR]}")
        typer.Exit(1)


@app.command()
def find(title: str) -> None:
    """
    View a single task.
    """
    task = TaskController()
    task.title = title

    try:
        task.find_task()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_READ_ERROR]}")
        typer.Exit(1)


@app.command()
def complete(title: str) -> None:
    """
    Complete a task
    """
    task = TaskController()
    task.title = title

    try:
        task.complete_task()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_WRITE_ERROR]}")
        typer.Exit(1)


@app.command()
def delete(title: str) -> None:
    """
    Delete a task
    """
    task = TaskController()
    task.title = title
    try:
        task.delete_task()
        typer.Exit()
    except Exception as e:
        print(e)
        print(f":warning: Error: {ERRORS[DB_WRITE_ERROR]}")
        typer.Exit(1)
