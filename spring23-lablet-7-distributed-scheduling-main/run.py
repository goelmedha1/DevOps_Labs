import argparse
import pandas as pd
from src.simulate import run_simulation

def main():
    parser = argparse.ArgumentParser(
        prog='run.py',
        description='Distributed Cluster Scheduler')
    parser.add_argument("-s", "--servers", default=5,
                        type=int, dest="servers")
    parser.add_argument("-t", "--simulation-time", default=1000,
                        type=int, dest="simulation_time")
    parser.add_argument("-u", "--utilizations",
                        default=[0.1, 0.2, 0.8, 0.9], nargs='+', dest="utilizations")
    parser.add_argument("-l", "--search-limit", type=int,
                        default=-1, dest="search_limit", help="Search Limit")
    parser.add_argument("-q", "--queue-threshold", type=int,
                        default=2, dest="queue_threshold", help="Queue Threshold")
    parser.add_argument("-p", "--policies", default=["receiver", "sender"], nargs="+",
                        dest="policies", choices=["sender", "receiver"])

    args = parser.parse_args()
    results = []
    if args.search_limit == -1:
        args.search_limit = args.servers
    for utilization in args.utilizations:
        for policy in args.policies:
            df = run_simulation(args.servers, args.simulation_time,
                                     utilization, policy, args.search_limit, args.queue_threshold)
            results.append(df)
            print(
                f"Policy: {policy[0]}, Utilization: {utilization} = Messages->{df['messages'].mean()}, Migrations->{df['migrations'].mean()}")

    results = pd.concat(results)
    results.to_csv(
        f"results-{args.servers}-{args.simulation_time}-{args.queue_threshold}-{args.search_limit}.csv", index=False)


if __name__ == "__main__":
    main()