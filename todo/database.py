from todo import config

# Categories - id, title
categories_table_query = """CREATE TABLE IF NOT EXISTS categories(
    id SERIAL PRIMARY KEY,
    title varchar(255) NOT NULL
)"""

# Priorities - id, title
priorities_table_query = """CREATE TABLE IF NOT EXISTS priorities(
    id SERIAL PRIMARY KEY,
    title varchar(255) NOT NULL
)"""

# Tasks - title, due date, priority, category, completed
tasks_table_query = """CREATE TABLE IF NOT EXISTS tasks(
    id SERIAL PRIMARY KEY,
    title varchar(255) NOT NULL,
    due_date timestamp NOT NULL,
    priority integer,
    FOREIGN KEY(priority) REFERENCES priorities(id),
    category integer,
    FOREIGN KEY(category) REFERENCES categories(id),
    completed boolean DEFAULT false
)"""

# To do - title, priority, category, date, completed
todo_table_query = """CREATE TABLE IF NOT EXISTS todos(
    id SERIAL PRIMARY KEY,
    title varchar(255) NOT NULL,
    date timestamp NOT NULL,
    priority integer,
    FOREIGN KEY(priority) REFERENCES priorities(id),
    category integer,
    FOREIGN KEY(category) REFERENCES categories(id),
    completed boolean DEFAULT false
)"""

queries = [
        categories_table_query,
        priorities_table_query,
        todo_table_query,
        tasks_table_query,
        ]


def create_tables():
    conn, cursor = config.connect_to_db()
    for query in queries:
        cursor.execute(query)
        conn.commit()
