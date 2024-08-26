__app_name__ = "todo"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    DB_ERROR,
    ID_ERROR,
    INITIALIZATION_ERROR
) = range(8)

ERRORS = {
    DIR_ERROR: "Config directory error",
    FILE_ERROR: "Config file error",
    DB_READ_ERROR: "Failed to read!",
    DB_WRITE_ERROR: "Failed to write!",
    DB_ERROR: "Failed to connect to database",
    ID_ERROR: "Invalid ID",
    INITIALIZATION_ERROR: "Failed to initialize app"
}
