import os

from locust import HttpLocust, TaskSet, task, between

# Multriple users in SSO?
# Faked SSO env
# Hawk - extra layer of protection

# We also need a locust test that hammers the edit POST endpoint and the forecast view and pushes the PAAS set up until it falls over.


class UserBehaviour(TaskSet):
    # def on_start(self):
    #     """ on_start is called when a Locust start before any task is scheduled """
    #     self.login()
    #
    # def on_stop(self):
    #     """ on_stop is called when the TaskSet is stopping """
    #     self.logout()
    #
    # def login(self):
    #     self.client.post("/login", {"username":"ellen_key", "password":"education"})
    #
    # def logout(self):
    #     self.client.post("/logout", {"username":"ellen_key", "password":"education"})

    @task(2)
    def index(self):
        headers = {
            "Cookie": f"csrftoken={os.environ['CRSF_TOKEN']}; sessionid={os.environ['SESSION_ID']}"
        }

        self.client.get("", headers=headers)

    # @task(1)
    # def profile(self):
    #     self.client.get("/profile")


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
