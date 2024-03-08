## Install Pyro

To install Pyro5, simply run
```
pip3 install pyro5
```

## How to Run

See https://pyro5.readthedocs.io/en/latest/intro.html for how to run this code

There are two versions:
* Simple version: `greeting-server-simple.py` and `greeting-client-simple.py` use pyro5 without
using a name server. The object name has to be provided as input to the client.

* The version `greeting-server.py` and `greeting-client.py` use a name server and needs the Pyro
name server to be started (by running `pyro5-ns`).
