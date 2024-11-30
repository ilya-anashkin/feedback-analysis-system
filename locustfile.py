from random import randint
from time import sleep

from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def start_feedback(self):
        self.client.post("/api/feedback/start")

    @task
    def get_feedback_info(self):
        sleep(randint(0, 15))
        self.client.get("/api/feedback/info")

    @task
    def stop_feedback(self):
        sleep(randint(0, 60))
        self.client.post("/api/feedback/stop")
