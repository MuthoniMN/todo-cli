from todo.config import connect_to_db
from todo.helpers import create_or_find
from datetime import date
from typing import Any, List, Tuple
from rich import print
from rich.table import Table
from todo.tasks import TaskController

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

# Creating a to-do

    def create_todo(self) -> None:
        query = """INSERT INTO todos
                    (title, date, priority, category)
                    VALUES(%s, %s, %s, %s)"""
        category_id = create_or_find("categories", self.category, cursor, conn)
        priority_id = create_or_find("priorities", self.priority, cursor, conn)
        values = (
            self.title,
            self.date,
            priority_id,
            category_id
        )

        print(":hourglass_flowing_sand: Creating task...")
        cursor.execute(query, values)
        conn.commit()
        print(":white_check_mark: Task successfully created:confetti_ball:")

# List today's to-do

    def list_todos(self) -> List[Tuple[Any, ...]]:
        today = date.today()
        fetch_query = """
            SELECT todos.title, categories.title, priorities.title, todos.completed
            FROM ((todos
            INNER JOIN categories ON todos.category = categories.id)
            INNER JOIN priorities ON todos.priority = priorities.id)
            WHERE date = %s
            """
        print(":hourglass_flowing_sand: Fetching to-do list")
        cursor.execute(fetch_query, (today,))
        values = cursor.fetchall()

        print(":confetti_ball: To-do list successfully fetched!")
        print("---------------------------------")
        if len(values) == 0:
            print(":heavy_exclamation_mark: No tasks added yet!")
            print("-------------------------------")
            tasks = TaskController()
            tasks.list_tasks(7)
            return
        print(f":writing_hand_medium-light_skin_tone: To-do list for {today}")
        print("-------------------------------")

        table = Table("task", "category", "priority", "completed")
        for task in values:
            completion = ":cross_mark:"
            title, category, priority, completed = task
            if completed:
                completion = ":white_check_mark:"
            table.add_row(title, category, priority, completion)
        print(table)
        print("-------------------------------")

        tasks = TaskController()
        tasks.list_tasks(7)
        return

# display a to-do

    def find_todo(self) -> Tuple[Any, ...]:
        today = date.today()
        fetch_query = """
            SELECT todos.title, categories.title, priorities.title, todos.completed
            FROM ((todos
            INNER JOIN categories ON todos.category = categories.id)
            INNER JOIN priorities ON todos.priority = priorities.id)
            WHERE todos.date = %s AND todos.title = %s
            """

        cursor.execute(fetch_query, (today, self.title))
        print(":hourglass_flowing_sand: Fetching task")
        value = cursor.fetchone()
        if value is None:
            print(":heavy_exclamation_mark: Task was not found")
        else:
            print(":confetti_ball: Task successfully fetched!")
            table = Table("task", "completed")
            completion = ":cross_mark:"
            title, completed = value
            if completed:
                completion = ":white_check_mark:"
            table.add_row(title, completion)
            print(table)

# complete a to-do

    def complete_todo(self) -> None:
        today = date.today()
        update_query = """UPDATE todos
                        SET completed = true
                        WHERE date = %s AND title = %s"""
        fetch_query = """
            SELECT todos.title, categories.title, priorities.title, todos.completed
            FROM ((todos
            INNER JOIN categories ON todos.category = categories.id)
            INNER JOIN priorities ON todos.priority = priorities.id)
            WHERE todos.date = %s AND todos.title = %s
            """
        print(":hourglass_flowing_sand: Completing task...")
        cursor.execute(update_query, (today, self.title))
        conn.commit()
        cursor.execute(fetch_query, (today, self.title))
        value = cursor.fetchone()
        if value is None:
            print(":heavy_exclamation_mark: Failed to complete task")
        else:
            print(":white_check_mark: Completed task successfully!")

# deleting a to-do

    def delete_todo(self) -> None:
        today = date.today()
        print(":hourglass_flowing_sand: Deleting task...")
        query = "DELETE from todos WHERE date = %s AND title = %s"

        cursor.execute(query, (today, self.title))
        conn.commit()
        print(":white_check_mark: Deleted task successfully!")
