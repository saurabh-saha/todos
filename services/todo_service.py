import requests
from constants import HTTP_OK
from error import FetchTodoError
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def fetch_id(todo_id):
    """
    Fetches a single TODO item from the API.

    Args:
        todo_id (int): id to fetch.

    Returns:
        dict: A dictionary representing the fetched TODO item.
    Raises:
        FetchTodoError: If the TODO item could not be fetched.
    """
    url = f"{BASE_URL}{todo_id}"
    response = requests.get(url)

    if response.status_code != HTTP_OK:
        raise FetchTodoError(f"Failed to fetch TODO with ID {todo_id}. Status code: {response.status_code}")

    return response.json()
