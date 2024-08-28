from psycopg2.errors import ProgrammingError
from rich import print


def create(create_query, find_query, type, value, db, conn) -> int:
    db.execute(create_query, (value,))
    conn.commit()
    db.execute(find_query, (value,))
    created = db.fetchone()
    created_id, title = created
    if type == "categories":
        print(":white_check_mark: Created the category:balloon:")
        type = 'Category'
    elif type == "priorities":
        print(":white_check_mark: Created the priority:balloon:")
    return created_id


def create_or_find(type: str, value: str, db, conn) -> int:
    create_query = f"INSERT INTO {type} (title) VALUES(%s);"
    find_query = f"SELECT * FROM {type} WHERE title=%s LIMIT 1;"

    db.execute(find_query, (value,))
    print(f":hourglass_flowing_sand: Fetching {type}...")
    try:
        fetched = db.fetchone()
        if fetched is None:
            print(f":heavy_exclamation_mark: {type} not found")
            print(f":hourglass_flowing_sand: Creating {type}...")
            return create(create_query, find_query, type, value, db, conn)
        else:
            fetched_id, title = fetched
            print(f":white_check_mark: Fetched {type}")
            return fetched_id
    except ProgrammingError:
        return create(create_query, find_query, type, value, db, conn)
