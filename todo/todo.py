from todo.database import connect_to_db
from datetime import date
from typing import Any, List, Tuple


class TodoController:
    def __init__(self) -> None:
        self.db = connect_to_db()

    def create_todo(todo, self) -> None:
        today = date.today()
        query = """INSERT INTO todos
                    (title date, priority, category)
                    VALUES(%s, %s, %s, %s)"""
        category_id = self.create_or_find("categories", todo.priority)
        priority_id = self.create_or_find("priorities", todo.category)
        values = (
            todo.title,
            today.timestamp,
            priority_id,
            category_id
        )

        self.db.execute(query, values)

    def list_todos(self) -> List[Tuple[Any, ...]]:
        today = date.today()
        fetch_query = "SELECT * FROM todos WHERE date = %s"

        self.db.execute(fetch_query, (today.timestamp(),))
        values = self.db.findmany()
        return values

    def find_todo(title, self) -> Tuple[Any, ...]:
        today = date.today()
        fetch_query = "SELECT * FROM todos WHERE date = %s AND title = %s"

        self.db.execute(fetch_query, (today.timestamp(), title))
        value = self.db.findone()
        return value

    def complete_todo(title, self) -> None:
        today = date.today()
        fetch_query = """UPDATE todos
                        SET complete = 'false'
                        WHERE date = %s AND title = %s"""

        self.db.execute(fetch_query, (today.timestamp(), title))
        value = self.db.findone()
        return value

    def delete_todo(title, self) -> None:
        today = date.today()
        query = "DELETE todos WHERE title = %s"

        self.db.execute(query, (today.timestamp(), title))

    def create_or_find(type: str, value: str, self) -> int:
        create_query = "INSERT INTO {type} (title) VALUES(%s)"
        find_query = "SELECT * FROM {type} WHERE title=%s"

        self.db.execute(find_query, (value,))
        fetched = self.db.findone()

        if fetched is None:
            self.db.execute(create_query, (value,))
            created = self.db.findone()

            return created.id
        else:
            return fetched.id
