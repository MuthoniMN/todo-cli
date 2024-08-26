from typing import Optional
import typer
from todo import __app_name__, __version__, INITIALIZATION_ERROR, database

app = typer.Typer()


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
    try:
        database.create_tables()
        typer.echo("App initialized successfully!")
    except Exception as e:
        typer.echo(e)
        typer.echo(f"Error: {INITIALIZATION_ERROR}")
        typer.Exit(1)
