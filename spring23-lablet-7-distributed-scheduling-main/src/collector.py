import pandas as pd
from discrevpy import simulator
import numpy as np


class Collector:
    def __init__(self, servers) -> None:
        self.servers = servers
        self.server_logs = {}
        for i in range(1, servers + 1):
            self.server_logs[i] = []
        self.messages = 0
        self.migrations = 0

    def log(self, server_id, qlb, qla, messages, migrations):
        self.messages += messages
        self.migrations += migrations
        self.server_logs[server_id].append(
            {"qlb": qlb, "qla": qla, "messages": messages, "migrations": migrations, "time": simulator.now()})

    def get_results(self, server_id):
        df = pd.DataFrame.from_dict(self.server_logs[server_id])
        return df["messages"].sum(), df["migrations"].sum(), df["qla"].mean()

    def print(self):
        messages = []
        migrations = []
        for i in range(1, self.servers + 1):
            msg, mig = self.get_results(i)
            messages.append(msg)
            migrations.append(mig)
        messages = np.array(messages).mean()
        migrations = np.array(migrations).mean()
        print(f" Messages: {messages} - Migrations: {migrations}")