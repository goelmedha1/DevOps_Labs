## Quick Start

Note: Some machines have issues running or compiling this code. Linux is the best option and MacOS with the right tools also works. If you have issues, it
is fine to read the code and understand it at a conceptual level.

Install dependencies:

- gcc
- make
- rpcbind
- rpcgen
- libtirpc-devel

Build project:

```
make
```

Start `rpcbind` service:

```
sudo rpcbind
```

Start the server:

```
./add_server
```

From another terminal, start the client:

```
./add_client localhost 1 2
```
