from todo.config import connect_to_db
from todo.helpers import create_or_find
from datetime import date, timedelta, datetime
from typing import Any, List, Tuple
from rich import print
from rich.table import Table

conn, cursor = connect_to_db()


class TaskController:
    def __init__(self) -> None:
        self.title = None
        self.category = None
        self.priority = None
        self.date = date.today()
        self.completed = False

    def __str__(self) -> str:
        return f"Task: {self.title}\nDate: {self.date}\nCategory: {self.category}\nPriority: {self.priority}"

# Creating a task

    def create_task(self) -> None:
        query = """INSERT INTO tasks
                    (title, due_date, priority, category)
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

    def list_tasks(self, duration) -> List[Tuple[Any, ...]]:
        today = date.today()
        fetch_query = f"""
            SELECT tasks.title, categories.title, 
            priorities.title, tasks.due_date, tasks.completed
            FROM ((tasks
            INNER JOIN categories ON tasks.category = categories.id)
            INNER JOIN priorities ON tasks.priority = priorities.id)
            WHERE tasks.due_date > NOW() - INTERVAL '{duration} days' 
            AND completed = false
            """
        print(":hourglass_flowing_sand: Fetching task list")
        cursor.execute(fetch_query)
        values = cursor.fetchall()
        print(":confetti_ball: Tasklist successfully fetched!")
        print("---------------------------------")
        if len(values) == 0:
            print(":heavy_exclamation_mark: No tasks added yet!")
            print("-------------------------------")
            return
        print(f":writing_hand_medium-light_skin_tone: Tasks due between {today} and {today + timedelta(days=duration)}")
        print("-------------------------------")

        table = Table("task", "category", "priority", "due date", "completed")
        for task in values:
            completion = ":cross_mark:"
            title, category, priority, due_date, completed = task
            if completed:
                completion = ":white_check_mark:"
            table.add_row(title, category, priority, f"{due_date}", completion)
        print(table)
        print("-------------------------------")

# display a to-do

    def find_task(self) -> Tuple[Any, ...]:
        fetch_query = """
            SELECT tasks.title, categories.title, priorities.title, tasks.due_date, tasks.completed
            FROM ((tasks
            INNER JOIN categories ON tasks.category = categories.id)
            INNER JOIN priorities ON tasks.priority = priorities.id)
            WHERE tasks.title = %s
            """

        cursor.execute(fetch_query, (self.title, ))
        print(":hourglass_flowing_sand: Fetching task...")
        value = cursor.fetchone()
        if value is None:
            print(":heavy_exclamation_mark: Task was not found")
        else:
            print(":confetti_ball: Task successfully fetched!")
            table = Table("task", 
                          "category", 
                          "priority", 
                          "due date", 
                          "completed")
            completion = ":cross_mark:"
            title, category, priority, date, completed = value
            if completed:
                completion = ":white_check_mark:"
            table.add_row(title, category, priority, f"{date}", completion)
            print(table)

# complete a to-do

    def complete_task(self) -> None:
        update_query = """UPDATE tasks
                        SET completed = true
                        WHERE title = %s"""
        fetch_query = """
            SELECT tasks.title, categories.title, priorities.title, tasks.due_date, tasks.completed
            FROM ((tasks
            INNER JOIN categories ON tasks.category = categories.id)
            INNER JOIN priorities ON tasks.priority = priorities.id)
            WHERE tasks.title = %s
            """
        print(":hourglass_flowing_sand: Completing task...")
        cursor.execute(update_query, (self.title, ))
        conn.commit()
        cursor.execute(fetch_query, (self.title, ))
        value = cursor.fetchone()
        if value is None:
            print(":heavy_exclamation_mark: Failed to complete task")
        else:
            print(":white_check_mark: Completed task successfully!")

# deleting a to-do

    def delete_task(self) -> None:
        print(":hourglass_flowing_sand: Deleting task...")
        query = "DELETE from tasks WHERE title = %s"

        cursor.execute(query, (self.title, ))
        conn.commit()
        print(":white_check_mark: Deleted task successfully!")
