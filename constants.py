import os

HTTP_OK = 200
BASE_URL = "https://jsonplaceholder.typicode.com/todos/"
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_cache.json")
CACHE_EXPIRY_SECONDS = 3600
