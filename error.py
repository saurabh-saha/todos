class FetchTodoError(Exception):
    """Custom exception class for fetch_todo errors."""
    def __init__(self, message):
        super().__init__(message)
