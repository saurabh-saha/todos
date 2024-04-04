import unittest
from unittest.mock import patch
from cli import fetch_todo_with_cache, get_all_todos
from models.cache import Cache
from models.todo import Todo


class TestFetchTodoWithCache(unittest.TestCase):
    @patch('cli.requests.get')
    def test_fetch_todo_with_cache_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": False
        }
        todo = fetch_todo_with_cache(1)
        self.assertIsInstance(todo, Todo)
        self.assertEqual(todo.title, "delectus aut autem")

    @patch('cli.requests.get')
    def test_fetch_todo_with_cache_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        todo = fetch_todo_with_cache(1)
        self.assertIsNone(todo)

    @patch('cli.requests.get')
    def test_get_all_todos(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {"userId": 1, "id": 1, "title": "delectus aut autem", "completed": False},
            {"userId": 1, "id": 2, "title": "quis ut nam facilis et officia qui", "completed": True}
        ]
        todos = get_all_todos()
        self.assertIsInstance(todos[0], Todo)
        self.assertEqual(todos[0].title, "delectus aut autem")
        self.assertEqual(todos[1].completed, True)


if __name__ == '__main__':
    unittest.main()
