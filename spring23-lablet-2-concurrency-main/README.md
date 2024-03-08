[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10237882&assignment_repo_type=AssignmentRepo)
# Lablet 2: Concurrent Programming for Networked Servers

In this hands-on lablet, we will delve deeper into the various concurreny models for server applications
that we covered in class. The goal is understand how to use concurrency to imeplement servers that use the thread-per-request model
the thread pool model, and the asyncronous event model.


This homework has four parts, each part is an implementation of the same toy client-server
application but using a different approach for concurrent programming on the server side. Our
application does the following things: a client sends a message to the server, the server reverses
the message string and send the reversed string as reply to the client. The server is designed to be
concurrent and can service multiple client requests using one of the above models.

We have provide the code for all four parts. You are expected to read and understand code. You also
need to run the code examples on your local machine as well as Edlab machines.

## Part 1: Thread-per-request Model

Look at the example code provided in the [thread-per-request](/thread-per-request/) directory. For
this part you can use either the python version or the java version. First run both the server and
the clients on your local machine, then run them on two different Edlab machines (you will need to
change the ip addresses in the code and maybe port number if other people are also running the
experiment at the same time). Try connecting multiple clients at the same time and observe what
happens.

## Part 2: Thread-per-session Model

Look at the example code provided in the [thread-per-session](/thread-per-session/) directory. For
this part you can use either the python version or the java version. First run both the server and
the clients on your local machine, then run them on two different Edlab machines (you will need to
change the ip addresses in the code and maybe port number if other people are also running the
experiment at the same time). Try connecting multiple clients at the same time and observe what
happens.

Read the code carefully and pay attention how the code is different from part 1. Essentially, in
part 1 the client opens a new connection for each request, while in this part the client will send
multiple requests on the same connection (i.e., session).

## Part 3: Threadpool Model

Look at the example code provided in the [threadpool](/threadpool/) directory. For this part you
can also choose either the python version or the java version. First run both the server and the
clients on your local machine, then run them on two different Edlab machines.

Finally, run one server instance with three clients running at the same time. Do you observe any
problems? What if you close one of the clients? Describe how you can solve the problem and briefly
explain in the [README file](threadpool/README.md). Hint: There are two possible solutions. One method involves changing the server code and requires no changes to the client code. Another method changes the client code and requires no changes to the server code. Try to figure out both solutions.

## Part 4: Asynchronous Programming

Look at the example python code provided in the [async](/async/) directory. Run the code on your
local machine as well as Edlab machines. Try connecting multiple clients at the same time and
observe what happens.

## What to Submit

This is a tutorial-style lablet where we have provided most of the code for you. The goal is to
learn the concepts by reading the code and running it. In some cases, minor modifications may be
needed to get the code to run in your environment.

You can turn in your modified github repo via github classroom. In each folder, you should include
a) the modified code (if modifications were needed) and b) an output.txt file or screenshots showing
output produced by your program for that question. You will get full credit if you simply complete
the required questions. Also submit your work on gradescope.

Note that for part 1 to 3 we have provided both a python version and a java version. In your
submission please delete the version that you didn't use. This will make our grading process easier.
