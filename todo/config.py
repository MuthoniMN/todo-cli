from dotenv import load_dotenv
import typer
import os
import psycopg2
from todo import (
    DB_ERROR,
)

load_dotenv()


def connect_to_db():
    try:
        conn = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        return conn, conn.cursor()
    except Exception:
        typer.echo(f"Error: {DB_ERROR}")
        typer.exit()
