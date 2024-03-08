# Lablet 7: Distributed Scheduling
The lablet aims to introduce performance gains and overheads of distributed scheduling policies in various scenarios. Distributed scheduling can be implemented with many goals in mind such as load balancing, efficient placement, etc. In this lablet we focus on the load balancing and evaluate the performance of the receiver-initiated and server-initiated policies described here. 

## Instructions
The experiments and full instructions is available on [this jupyter notebook](runme.ipynb). 

## Simulation
This lablet uses discrete time simulation using [discrevpy](https://snkas.github.io/discrevpy/).

Lablet structure
```
.
├── README.md # current file
├── requirements.txt # requirements
├── run.py # cmd interface to run the simulation with different options
├── runme.ipynb # lablet notebook.
└── src # code
    ├── __init__.py
    ├── cluster.py
    ├── collector.py
    ├── server.py
    ├── simulate.py
    └── task.py
```
## Running the lab.
Installation
```
pip3 install -r requirements.txt
```

The lablet is designed to be executed from the jupyter notebook as mentioned earlier. The simulation have another console interface `run.py`. However, you don't need to use this for this lablet.
```
python3 run.py -h
usage: run.py [-h] [-s SERVERS] [-t SIMULATION_TIME] [-u UTILIZATIONS [UTILIZATIONS ...]] [-l SEARCH_LIMIT] [-q QUEUE_THRESHOLD] [-p {sender,receiver} [{sender,receiver} ...]]

Distributed Cluster Scheduler

options:
  -h, --help            show this help message and exit
  -s SERVERS, --servers SERVERS
  -t SIMULATION_TIME, --simulation-time SIMULATION_TIME
  -u UTILIZATIONS [UTILIZATIONS ...], --utilizations UTILIZATIONS [UTILIZATIONS ...]
  -l SEARCH_LIMIT, --search-limit SEARCH_LIMIT
                        Search Limit
  -q QUEUE_THRESHOLD, --queue-threshold QUEUE_THRESHOLD
                        Queue Threshold
  -p {sender,receiver} [{sender,receiver} ...], --policies {sender,receiver} [{sender,receiver} ...]
```


## What to submit
The notebook contains multiple scenarios and questions. Please answer the questions in the notebook.

Grading rubric:
- Part 1 (25%)
- Part 2 (25%)
- Part 3 (25%)
- Part 4 (25%)