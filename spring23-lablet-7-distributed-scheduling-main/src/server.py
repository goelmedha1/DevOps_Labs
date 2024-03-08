from typing import List
from src.task import Task, State
from discrevpy import simulator
from numpy.random import exponential


class Server:
    def __init__(self, cluster, id, threshold, arrival_rate, service_rate, policy) -> None:
        self.cluster = cluster
        self.ID = id
        self.threshold = threshold
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.policy = policy
        self.task_queue: List[Task] = []
        self.running_task: Task = None
        self.total_tasks = 0
        self.total_time = 0

        simulator.schedule(0, self.submit_task)
        simulator.schedule(0, self.run)

    def send_task(self, task) -> bool:
        if len(self.task_queue) < self.threshold:
            self.task_queue.append(task)
            return True
        return False

    def get_task(self) -> bool:
        if len(self.task_queue) > self.threshold:
            task = self.task_queue[-1]
            del self.task_queue[-1]
            return task
        return None

    def add_task(self, task) -> bool:
        self.task_queue.append(task)

    def execute_policy(self):
        if simulator.now() % 1000 != 0:
            return
        qlb = len(self.task_queue)
        messages = 0
        migrations = 0
        candidate_servers = self.cluster.get_candidate_servers(self.ID)
        while len(candidate_servers) > 0:
            server = candidate_servers[0]
            del candidate_servers[0]
            if self.policy == "sender":
                while len(self.task_queue) > self.threshold:
                    task = self.task_queue[-1]
                    messages += 1
                    if server.send_task(task):
                        del self.task_queue[-1]
                        migrations += 1
                    else:
                        break
            else:
                while len(self.task_queue) < self.threshold:
                    messages += 1
                    task = server.get_task()
                    if task:
                        self.task_queue.append(task)
                        migrations += 1
                    else:
                        break
        qla = len(self.task_queue)
        self.cluster.collector.log(self.ID, qlb, qla, messages, migrations)

    def run(self):
        if self.running_task and self.running_task.state == State.RUN:
            pass
        else:
            if __debug__:
                if self.running_task:
                    assert self.running_task.state == State.DONE

            if len(self.task_queue) > 0:
                self.running_task = self.task_queue[0]
                del self.task_queue[0]
                self.running_task.run()
                self.total_tasks += 1
                self.total_time += self.running_task.service_time

        self.execute_policy()

        simulator.schedule(1, self.run)

    def submit_task(self):
        try:
            service_time = int(exponential(1000 / self.service_rate, size=1))
            task = Task(f"{self.ID}-{simulator.now()}", service_time)
            self.add_task(task)
            next_arrival_time = int(exponential(
                1000 / self.arrival_rate, size=1))
            simulator.schedule(next_arrival_time, self.submit_task)
        except:
            simulator.schedule(0, self.submit_task)

    def print(self):
        print(
            f"Server {self.ID}: Total tasks {self.total_tasks}, Used Time {self.total_time}")
