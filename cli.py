import os
import time
from concurrent.futures import ThreadPoolExecutor
from models.cache import Cache
import requests
from error import FetchTodoError
from dotenv import load_dotenv
from models.todo import Todo

load_dotenv()
CACHE_FILE = os.getenv("CACHE_FILE")
CACHE_EXPIRY_SECONDS = int(os.getenv("CACHE_EXPIRY_SECONDS", 60))
BASE_URL = os.getenv("BASE_URL")


def fetch_todo_with_cache(todo_id, cache=None):
    """
    Fetches a single TODO item from the API with caching support.

    Args:
        todo_id (int): The ID of the TODO item to fetch.
        cache (Cache): The Cache object.

    Returns:
        dict: The JSON response containing the TODO item.
    """
    url = f"{BASE_URL}{todo_id}"

    try:
        if cache:
            cached_response = cache.get_cached_response(url)
            if cached_response:
                print(f"Fetching TODO with ID {todo_id} from cache.")
                return cached_response

        todo_data = Todo.fetch(todo_id)

        if cache:
            cache.save_response_to_cache(url, todo_data.to_json())

        return todo_data
    except Exception as e:
        print(f"Error occurred while fetching TODO with ID {todo_id}: {e}")
        return None


def get_all_todos(num_todos=20, cache=None):
    """
    Fetches all TODO items from the API using ThreadPoolExecutor with caching support.

    Args:
        num_todos (int): Number of TODO items to fetch.
        cache (Cache): The Cache object.

    Returns:
        list: A list of Todo objects containing the fetched TODO items.
    """
    todo_responses = []
    todo_ids = [i * 2 for i in range(1, num_todos + 1)]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_todo_with_cache, todo_id, cache) for todo_id in todo_ids]

        for future in futures:
            todo_response = future.result()
            if todo_response:
                todo_responses.append(todo_response)

    return todo_responses


def display_todos(todo_responses):
    """
    Displays the titles and completion status of TODO items.

    Args:
        todo_responses (list): A list of Todo objects containing the fetched TODO items.
    """
    for todo in todo_responses:
        if todo:
            print(todo)
        else:
            print("Error: Unable to fetch TODO.")


def main():
    cache = Cache()
    cache.load_cache()

    start_time = time.time()
    todo_responses = get_all_todos(cache=cache)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")

    display_todos(todo_responses)


if __name__ == "__main__":
    main()
