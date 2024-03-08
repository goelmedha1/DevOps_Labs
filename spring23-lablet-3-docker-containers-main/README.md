[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-8d59dc4de5201274e310e4c54b9627a8934c3b88527886e3b421487c677d23eb.svg)](https://classroom.github.com/a/SFxE8aDL)
Compsci 677: Distributed and Operating Systems

Spring 2023

# Lablet 3: Docker

This lablet is a hands-on tutorial to use docker, dockerfile, and docker compose.

## Part 1: Install Docker
Please follow the installations for your operating system. However, It's recommended that you use a Linux machine or virtual machine for this tutorial.
### Linux

For Ubuntu please follow [this guide](https://docs.docker.com/engine/install/ubuntu/) to install
docker engine. If you are using other distros please refer to [this
page](https://docs.docker.com/engine/install/) to check if it's officially supported by Docker.

By default docker requires `root` privileges to run on Linux, therefore you will have to prefix all
the docker commands in this tutorial with `sudo` to run as `root`. If you don't want to run docker
commands without `sudo`, you can either [create a group named `docker` and add your user to this
group](https://docs.docker.com/engine/install/linux-postinstall/) (the `docker` group grants
privileges equivalent to the `root` user), or you can run the docker daemon in [rootless
mode](https://docs.docker.com/engine/security/rootless/) (this is more secure but has certain
limitations).

### Windows

Download and install [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/).
Depending on your Windows version, you may need to first [enable WSL 2 or
Hyper-V](https://docs.docker.com/desktop/windows/install/#system-requirements) in order to
successfully install Docker Desktop. After installation please check out the [Docker Desktop for
Windows user manual](https://docs.docker.com/desktop/windows/) for Windows specific settings.

### Mac

Download and install [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/). After
installation please check out the [Docker Desktop for Mac user
manual](https://docs.docker.com/desktop/mac/) for Mac specific settings. The Docker Desktop for mac comes with versions for intel based CPUs and apple silicon CPUs as well. 

### Notes on Docker Desktop

Docker uses a client-server architecture. The docker cli that we use to run docker commands is the
client. It communicates with the docker daemon (the server) over a socket. However, the docker
daemon cannot run natively on Windows or Mac due to certain required capabilities are missing on
those platforms. Therefore, docker provides Docker Desktop for Windows and Mac, which actually
starts a virtual machine in the background and run the docker daemon inside that VM. This extra VM
layer can sometimes lead to unexpected problems. Therefore, we recommend using using a Linux machine
or virtual machine for this tutorial.

## Part 2: Basic Usage

### Check Docker Version

First you should verify whether docker is installed successfully. Run

```shell
docker version
```

What is the docker version you are running? Record the output in your output file.

### Query Images on Docker Hub

By default docker can query/pull/push images on the Docker Hub public registry. To query images
matching the name `redis`, run

```shell
docker search redis
```

You can also search for images on the [Docker Hub webpage](https://hub.docker.com).

### Download (Pull) an Image

```shell
docker pull redis
```

After the `docker pull` command completes, verify the image has been successfully downloaded using

```shell
docker images
```

### Start a Docker Container

To start a docker container using the `redis` image we just downloaded, run

```shell
docker run --name my_redis -d redis
```

The `--name my_redis` parameter tells docker to name the started container `my_redis`. If you don't
specify a name docker will generate a random name for the container. The `-d` parameter means the
containers should be started in the background (detached mode) so that your terminal isn't blocked
by the started container.

After the container has been started, verify that it's running using

```shell
docker ps
```

Although the container is started in detached mode, we can still check its output using the `docker
logs` command.

```shell
❯ docker logs my_redis
1:C 19 Mar 2022 03:47:05.868 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 19 Mar 2022 03:47:05.868 # Redis version=6.2.6, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 19 Mar 2022 03:47:05.868 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
1:M 19 Mar 2022 03:47:05.868 * monotonic clock: POSIX clock_gettime
1:M 19 Mar 2022 03:47:05.869 * Running mode=standalone, port=6379.
1:M 19 Mar 2022 03:47:05.869 # Server initialized
1:M 19 Mar 2022 03:47:05.869 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
1:M 19 Mar 2022 03:47:05.869 * Ready to accept connections
```

Here we can see that redis server is running on port 6379 of the `my_redis` container.

### Run Commands on a Running Container

You can run commands on a running container using the `docker exec` command. The most common use
case is to get an interactive shell on a container, which can be useful when debugging an
application running inside a container. For example, to get a `bash` shell on the `my_redis`
container:

**Note:** Don't forget to stop and remove the older container as container names are unique.
```shell
docker stop my_redis
docker rm my_redis
```
Then to start the container in interactive mode.

```shell
docker run -it --name my_redis redis bash
```

Run the command above to obtain an interactive `bash` shell. You will notice that a lot of commands
are missing here in order to reduce the docker image size to a minimum. But you can still install
packages that you need. Install `htop` using `apt update && apt install -y htop` (you don't need
`sudo` because the default user is `root`). Start `htop` and observe the system resources and
processes. How many CPU cores, memory, and processes are there? Record the output in your output
file.

### Access a Container Using IP Address

Note that to communicate with the `my_redis` container, we still need to have its IP address. We can
get the IP address of `my_redis` using

```shell
docker inspect my_redis
```

This command will generate a lot of output, but there should be a line that starts with
`"IPAddress":` followed by the IP address of the container. In my case it's `172.17.0.2`.

Let run a client to interact with the `redis` server. Here we use the Redis Python client. First
install it using

```shell
pip3 install redis
```

Now let's start a Python REPL and verify that we can talk with the redis server on
`172.17.0.2:6379`:

```python
>>> import redis
>>> r = redis.Redis(host='172.17.0.2', port=6379)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
```

**Note:** If you are using Docker Desktop on macos or windows you will need to make sure that the network inside the VM is accessible. However, an easier/recommended solution is to Export the network to the host (more details on port forwarding later). Docker Desktop will make the exported ports available to the host network. Ex: `docker run -it --name my_redis -p 6379:6379 redis bash`

## Part 3: Build a Docker Image using a Custom Dockerfile

Now we build a web application that uses redis as the cache server/database. Many Internet content
providers store view count information, e.g., how many times a Piazza post has been viewed or how
many times a YouTube video has been watched. We have implemented a simple application that tracks
how many times a web page has been viewed in `view_count.py`. Read the code and make sure you
understand how it works.

To run this application, first install flask:

```shell
pip3 install flask
```

Then start the application using
```shell
REDIS_HOST="172.17.0.2" python3 view_count.py
```

Here we are passing the redis host as an environment variable because the IP address of the redis
server might change in the future. If we hardcode the IP address, we will have to modify the source
code. And when we containerize our application later, every time we change the source code we will
have to rebuild our docker image! Therefore, we are passing the redis host as an environment
variable to avoid this problem.

No open a browser and open `127.0.0.1:8080`, you should see the message "This page has been viewed 1
times." Every time you refresh this page the counter will increase by 1.

Now we will build a docker image for our application. A dockerfile is required to build a docker
image. We have provided a dockerfile for you. The contents are listed as follows

```Dockerfile
FROM python:3.8-alpine

RUN pip install flask redis

WORKDIR /app

COPY view_count.py .

ENTRYPOINT ["python", "view_count.py"]
```

The meaning of each line is:

1. `FROM python:3.8-alpine` means we are using the official python image as the _base layer_ for our
   image. Docker images is built up from a series of layers. Each layer except the very last one is
   read-only: every time we use a command to update a layer, a new layer is generated. Since we our
   app is written in Python we use the official python image as our base layer.

   The `3.8-alpine` after the colon specifies the _tag_ we want to use for the python image. Tags
   are mutable references to different versions/variants of images with the same name. For example,
   for python you can choose from tags `3.7`, `3.8`, `3.9`, etc., which have different python
   versions running inside. Here we are using `3.8-alpine` which means it's built with Python 3.8
   installed from the `alpine` base image.

2. `RUN pip install flask redis` runs the `pip install` command to install the dependencies for our
   application. We are using one `pip install` command to install two packages at the same time so
   only one new layer is generated. If we have two commands `RUN pip install flask` and `RUN pip
   install redis` then two layers will be generated. Generally speaking it's a good idea to minimize
   the number of layers in your dockerfile.

3. `WORKDIR /app` means wre are using `/app` as our working directory inside the docker image.
   Docker will create this directory for us automatically.

4. `COPY view_count.py .` tells docker to copy our application source file into the docker image. We
   can use `.` as the destination because we have already specified the working directory in our
   previous command.

5. `ENTRYPOINT ["python", "view_count.py"]` means that the command `python view_count.py` will be
   executed when our docker image is launched using the `docker run` command. Again we don't have to
   provide the absolute path to `view_count.py` since we have already specified `/app` as our
   working directory.

To build our image simply run
```
docker build . -t view_count
```

`.` means using the current folder as the working directory for building the image. `-t view_count`
means the built image should be tagged with the name `view_count`.

Now we can start our application using the `docker run` command:

```shell
docker run --name view_count --env REDIS_HOST=172.17.0.2 -d view_count
```

### Port Forwarding to a Container

Our application container should start successfully, but if you go to `127.0.0.1:8080` again in a
browser you won't be able to connect to our application. Why is that? Well, this is because our
application is now listen on port 8080 of the docker container, while your browser is trying to
connect to port `8080` of your host machine.

To solve this problem we need to create a port forwarding when we start our application container.
First stop and remove the container that is already running.

```shell
docker stop view_count
```

The `docker stop` command will stop a running container and free the cpu/memory used by that
container. Stopped containers remain on you disk: intermediate results produced will still be
stored. Also you cannot reuse the container name even if the container has been stopped. To
completely remove a container, use the `docker rm` command

```shell
docker rm view_count  # free disk space and the container name
```

Now restart our application with port forwarding enabled:

```shell
docker run --name view_count --env REDIS_HOST=172.17.0.2 -p 8080:8080 -d view_count
```

The `-p 8080:8080` means incoming connection to port `8080` on the host machine will be
automatically forwarded to port `8080` of the `view_count` container. This is done using a bridge
network that is automatically created when you install docker.

Now when you go to `127.0.0.1:8080` you should be able to access our application again.

#### Exercise 1

Let's make our view count page more fun by adding some emoji. Modify `Dockerfile` to
install the `emoji` package. Then modify `view_count` to add an :eye: (`:eye:`) at the beginning of
the returned message. Hint: use the`emoji.emojize()` function.

### Mount Docker Volumes

Remember that intermediate results produced in the container are only temporarily stored inside the
container and will be erased when the container is removed. Therefore, if we stop and remove the
`my_redis` container, our view count record will be erased. Next time we restart the redis container
the view count will start over from 0 (you can verify this your self).

To persist the results outside the container, we need to mount a directory on the host machine as a
volume in the container. This way all the results written to this volume will also be persisted in
the directory on the host machine.

First stop and remove the running containers

```shell
docker stop view_count my_redis
docker rm view_count my_redis
```

Then restart the redis container with volume mounted:

```shell
docker run --name my_redis --volume `pwd`/data:/data -d redis
docker run --name view_count --env REDIS_HOST=172.17.0.2 -p 8080:8080 -d view_count
```

The ``--volume `pwd`/data:/data`` means mount the `data` folder in our current directory to the
`/data` directory inside the container, which is the default location for data persistence used by
redis. In the case of Docker Desktop this directory is on the virtual machine, but you can still access via shared files option under `Settings/Resources/File Sharing`

Now go to `127.0.0.1:8080` and refresh the page a few times. Then stop and remove both containers

```
docker stop view_count my_redis
docker rm view_count my_redis
```

You should a `dump.rdb` file under the `data` folder. Note that you need to stop the `view_count`
container first because save is triggered when our view count application exits. If you stop the
`my_redis` container first the data won't be saved.

Now if you start the redis and view count application again, you will see that the view count will
continue from the previous value.

## Part 4: Orchestrating Multiple Docker Containers using Docker Compose

It's quite painful that every time we start our redis and view count application we will have to
type the `docker run` commands with many parameters. Also remember that the IP address of the redis
container may change. If you have other containers already running its IP address most likely will
not be `172.17.0.2`. So we would have to inspect the started redis container to know its IP and then
pass it to the view count container. Surely you can use shell scripts to automate these steps, but
docker provides a more elegant solution which is called docker compose.

### Install Docker Compose

If you are using Docker Desktop for Windows/Mac then docker compose is already installed. If you are
using Linux the easiest way to get docker compose is to download a prebuilt binary. You can follow
the steps described
[here](https://docs.docker.com/compose/install/#install-compose-on-linux-systems).

### `docker-compose.yml`

Docker compose is an easy way to orchestrate multiple containers using a yaml config file (it's
named `docker-compose.yml` by default). We have provided a `docker-compose.yml` for you:

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - redis
  redis:
    image: redis
    volumes:
      - ./data:/data
```

You can now start the two containers simply using

```shell
docker-compose up
```

This will block your current terminal and print output generated by all the created containers. If
you want to used the detached mode you can add the `-d` parameter.

Open another terminal and run `docker ps`. How many containers are there. What are the names of the
running containers? Record the output in your output file.

There are two things worth noting in the `docker-compose.yml`:

1. `depends_on` tells docker compose that when starting the containers it should first create the
   `redis` container, the `web` container should be created only when the `redis` container is in
   ready state. When stopping containers docker compose will stop them in the reverse order as they
   were created: it will first stop the `web` container then the `redis` container. This ensures
   data persistence works properly.

2. We are not passing the IP address as an environment variable anymore. If you read our application
   source you will see that when the environment variable is not set we will simply use the hostname
   `redis`. This is because by default docker compose sets up a single network for your app. Each
   container for a service joins the default network and is both reachable by other containers on
   that network, and discoverable by them at a hostname identical to the container name. So our view
   count application can now simply connect to the redis service using the hostname `redis`.

To stop and remove our app:
1. If you run `docker-compose up` in blocking mode, first run `Ctrl - C`. This stops the containers
   but does not remove them. To remove the containers you need to also run `docker-compose rm`.

2. If you run `docker-compose up` in detached mode, you can run `docker-compose down`. This will
   both stop and remove all the containers in the app.

#### Exercise 2

Modify `docker-compose.yml` and `view_count.py` so that the application runs on port `80`
inside the container. On the host machine it should still listens on port `8080`

## What to submit

An output file that contains the output required in the following sections:

* [Check Docker Version](#check-docker-version)
* [Run Commands on a Running Container](#run-commands-on-a-running-container)
* [`docker-compose.yml`](#docker-composeyml)

Also modify `view_count.py`, `Dockerfile`, and `docker-compose.yml` to complete the exercises [1](#exercise-1) and [2](#exercise-2).

## References

1. Dockerfile reference: https://docs.docker.com/engine/reference/builder/
2. Docker Compose file reference: https://docs.docker.com/compose/compose-file/compose-file-v3/
3. Networking in Compose: https://docs.docker.com/compose/networking/
4. Use volumes: https://docs.docker.com/storage/volumes/
