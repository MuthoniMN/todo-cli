from todo.config import connect_to_db
from todo.helpers import create_or_find
from datetime import date
from typing import Any, List, Tuple
from rich import print

conn, cursor = connect_to_db()


class TodoController:
    def __init__(self) -> None:
        self.title = None
        self.category = None
        self.priority = None
        self.date = date.today()
        self.completed = False

    def __str__(self) -> str:
        return f"Task: {self.title}\nDate: {self.date}\nCategory: {self.category}\nPriority: {self.priority}"

    def create_todo(self) -> None:
        query = """INSERT INTO todos
                    (title, date, priority, category)
                    VALUES(%s, %s, %s, %s)"""
        category_id = create_or_find("categories", self.category, cursor)
        priority_id = create_or_find("priorities", self.priority, cursor)
        values = (
            self.title,
            self.date,
            priority_id,
            category_id
        )

        print(":hourglass_flowing_sand: Creating task...")
        cursor.execute(query, values)
        print(":white_check_mark: Task successfully created:confetti_ball:")

    def list_todos(self) -> List[Tuple[Any, ...]]:
        today = date.today()
        fetch_query = "SELECT * FROM todos WHERE date = %s"

        cursor.execute(fetch_query, (today,))
        values = self.db.fetchmany()
        return values

    def find_todo(title, self) -> Tuple[Any, ...]:
        today = date.today()
        fetch_query = "SELECT * FROM todos WHERE date = %s AND title = %s"

        cursor.execute(fetch_query, (today, title))
        value = self.db.fetchone()
        return value

    def complete_todo(title, self) -> None:
        today = date.today()
        fetch_query = """UPDATE todos
                        SET complete = 'false'
                        WHERE date = %s AND title = %s"""

        cursor.execute(fetch_query, (today, title))
        value = self.db.fetchone()
        return value

    def delete_todo(title, self) -> None:
        today = date.today()
        query = "DELETE todos WHERE date = %s AND title = %s"

        cursor.execute(query, (today, title))
