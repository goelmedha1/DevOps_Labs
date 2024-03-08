from discrevpy import simulator
from src.cluster import create_cluster
from pandas import DataFrame
from numpy import random

random.seed(200)


def run_simulation(servers_number: int, simulation_time: int, utilization: int, policy: str, search_limit: int, queue_threshold: int) -> DataFrame:
    assert utilization > 0 and utilization < 1, "utilization must be between in (0, 1)"
    assert policy in ["sender", "receiver"], "Invalid Policy"
    assert servers_number > 0, "server number should be greater than 0"
    assert simulation_time > 300, "simulation time should be greater than 5 mins"

    try:
         simulator.reset()
    except:
        pass
    
    simulator.ready()
    cluster = create_cluster(
        servers_number, utilization, policy, search_limit, queue_threshold)
    simulator.end(simulation_time * 1000)
    simulator.run()
    simulator.reset()
    df = cluster.get_results()
    df["utilization"] = utilization
    df["policy"] = policy
    df["effective_utlization"] = df["total_time"] / \
        (1000 * simulation_time)
    return df
