from discrevpy import simulator
from enum import Enum


class State(Enum):
    QUEUED = 1
    RUN = 2
    DONE = 3


class Task:
    def __init__(self, id, service_time) -> None:
        self.ID = id
        self.service_time = service_time
        self.state = State.QUEUED

    def run(self):
        self.state = State.RUN
        self.finish_time = simulator.now() + self.service_time
        simulator.schedule(self.service_time, self.finish)

    def finish(self):
        assert simulator.now() == self.finish_time
        self.state = State.DONE