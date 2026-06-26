
import Pyro5.api
import json
import os
from datetime import datetime

@Pyro5.api.expose
class TaskQueue:

    def __init__(self):
        self.tasks = {}

        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)

                for task in self.tasks.values():
                    task["status"] = "pending"
                    task["result"] = None

            print("Tasks loaded successfully.")

        except FileNotFoundError:
            print("Error: tasks.json not found.")
            self.tasks = {}

    def request_task(self):

        for task_id, task in self.tasks.items():

            if task["status"] == "pending":

                task["status"] = "in-progress"

                print(f"Task {task_id} assigned.")

                return task_id, task

        return None

    def submit_result(self, task_id, result, worker_name):

        if task_id in self.tasks:

            self.tasks[task_id]["status"] = "completed"
            self.tasks[task_id]["result"] = result

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"[{timestamp}] [SUCCESS] Task {task_id} completed by {worker_name}. Result: {result}")

daemon = Pyro5.server.Daemon()

ns = Pyro5.api.locate_ns()

uri = daemon.register(TaskQueue)

ns.register("MasterServer", uri)

print("Master Server is running...")

daemon.requestLoop()
