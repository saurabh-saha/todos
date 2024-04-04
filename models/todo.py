from services.todo_service import fetch_id
from error import FetchTodoError


class Todo:
    """Class to represent a TODO item."""

    def __init__(self, todo_id, title=None, completed=None):
        """
        Initialize a Todo object.

        Args:
            todo_id (int): The ID of the TODO item.
            title (str, optional): The title of the TODO item. Defaults to None.
            completed (bool, optional): The completion status of the TODO item. Defaults to None.
        """
        self.todo_id = todo_id
        self.title = title
        self.completed = completed

    def __str__(self):
        """String representation of the Todo object."""
        return f"TODO ID: {self.todo_id}, Title: {self.title}, Completed: {self.completed}"

    def to_json(self):
        """
        Convert the Todo instance to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the Todo instance.
        """
        return {
            "id": self.todo_id,
            "title": self.title,
            "completed": self.completed
        }

    @classmethod
    def fetch(cls, todo_id):
        """
        Fetches a single TODO item from the API.

        Args:
            todo_id (int): The ID of the TODO item to fetch.

        Returns:
            Todo: A Todo object representing the fetched TODO item.
        """
        try:
            todo_data = fetch_id(todo_id)
            return cls(todo_id=todo_data.get("id"), title=todo_data.get("title"), completed=todo_data.get("completed"))
        except FetchTodoError as e:
            print(e)  # Handle error gracefully
            return None
