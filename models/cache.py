import os
import json
import time
import constants


class CachedResponse:
    """Class to represent a cached API response with timestamp."""

    def __init__(self, response):
        self.response = response
        self.timestamp = time.time()

    def format(self):
        """Format the cached response data."""
        return {"response": self.response, "timestamp": self.timestamp}


class Cache:
    """Class to handle caching of API responses."""
    def __init__(self):
        self.cache_file = constants.CACHE_FILE
        self.cache_expiry_seconds = constants.CACHE_EXPIRY_SECONDS
        self.cache_data = {}

    def load_cache(self):
        """Loads the cache data from the cache file into memory."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as file:
                self.cache_data = json.load(file)

    def get_cached_response(self, url):
        """
        Retrieves the cached response from the in-memory cache.

        Args:
            url (str): The URL of the API endpoint.

        Returns:
            dict: The cached response if found and valid, otherwise None.
        """
        cached_response = self.cache_data.get(url)
        if cached_response:
            timestamp = cached_response.get("timestamp")
            if time.time() - timestamp <= self.cache_expiry_seconds:
                return cached_response["response"]
        return None

    def save_response_to_cache(self, url, response):
        """
        Saves the API response to the cache file and in-memory cache.

        Args:
            url (str): The URL of the API endpoint.
            response (dict): The API response to cache.
        """
        self.cache_data[url] = CachedResponse(response).format()
        with open(self.cache_file, "w") as file:
            json.dump(self.cache_data, file)
