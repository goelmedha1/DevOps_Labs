from src.server import Server
from typing import List
from discrevpy import simulator
from src.collector import Collector
import random
import pandas as pd


class Cluster():

    def __init__(self, servers, search_limit) -> None:
        self.servers: List[Server] = []
        self.search_limit = search_limit
        self.collector = Collector(servers)

    def add_server(self, server: Server):
        self.servers.append(server)

    def get_candidate_servers(self, server_id) -> List[Server]:
        servers = []
        for server in self.servers:
            if server.ID != server_id:
                servers.append(server)
        random.shuffle(servers)
        servers = servers[0:self.search_limit]
        return servers

    def get_results(self):
        data = []
        for server in self.servers:
            messages, migrations, queue_length = self.collector.get_results(
                server_id=server.ID)
            l = [server.ID, server.total_tasks,
                 server.total_time, messages, migrations, queue_length]
            data.append(l)
        df = pd.DataFrame(
            data, columns=["server", "total_tasks", "total_time", "messages", "migrations", "queue_length"])
        return df

    def print(self):
        for server in self.servers:
            server.print()
        self.collector.print()


def create_cluster(servers_number: int, utilization: float, policy: str, search_limit:int, queue_threshold:int) -> Cluster:
    cluster = Cluster(servers_number, search_limit)
    service_rate = 20
    arrival_rate = utilization * service_rate
    for i in range(servers_number):
        server = Server(
            cluster, i + 1, queue_threshold, arrival_rate, service_rate, policy)

        cluster.add_server(server)
    return cluster
