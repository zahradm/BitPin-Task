import random
import string
import os
import django
from locust import HttpUser, task, between

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
# load the Django apps registry
django.setup()

class User(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000/"

    def on_start(self):
        # generate a random username for the test user
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        print('username')
        get_token_url = self.client.base_url + "user/token/"
        print(get_token_url)
        register_data = {"username": 'zahra', "password": "1234"}
        token_response = self.client.post(get_token_url, json=register_data)
        self.token = token_response.json()["access"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def add_rate(self):
        # create a cart for the test user
        rate_url = self.client.base_url + "api/posts/1/"
        rate = random.choice([1, 2, 3, 4, 5])
        rate_data = {"score": rate}
        cart_response = self.client.post(rate_url, headers=self.headers, json=rate_data)
        print(cart_response.json())





