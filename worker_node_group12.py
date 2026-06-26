worker node

import Pyro5.api
import random
import time
from datetime import datetime

worker_name = input("Enter Worker Name: ")

ns = Pyro5.api.locate_ns()

uri = ns.lookup("MasterServer")

master = Pyro5.api.Proxy(uri)

while True:

    seconds = random.randint(3,5)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] [SLEEPING] Pausing for {seconds} seconds...")

    time.sleep(seconds)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] [FETCHING] Requesting task from Master...")

    task = master.request_task()

    if task is None:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] [IDLE] No pending tasks available. Waiting...")

        continue

    task_id, data = task

    action = data["action"]

    values = data["values"]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] [COMPUTING] Task {task_id}: Performing {action} on {values}...")

    a, b = values

    if action == "add":
        result = a + b

    elif action == "subtract":
        result = a - b

    elif action == "multiply":
        result = a * b

    elif action == "divide":
        result = a / b

    else:
        result = None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] [SUBMITTING] Sending result {result} to Master...")

    master.submit_result(task_id, result, worker_name)
