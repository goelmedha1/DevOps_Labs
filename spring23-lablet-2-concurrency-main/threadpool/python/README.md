Run one server instance with three clients running at the same time. Do you observe any problems?
What if you close one of the clients? Describe how you can solve the problem and briefly explain. 

Hint: There are two possible solutions. One method involves changing the server code and requires 
no changes to the client code. Another method changes the client code and requires no changes to 
the server code.  Try to figure out both solutions.
 


---

_Write your answer here_

1. There was a problem when the third client was trying to connect as max workers allowed in the threadpool are 2.

2. Server side solution:-
   In order to solve this problem we can increase the maximum number of workers threads to handle increasing number of clients. 

   Client sie solution:- 
   We can use the time.sleep() function to introduce a delay between sending messages to the server.
