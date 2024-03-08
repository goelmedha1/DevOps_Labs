#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.simulate import *


# In[16]:


run_simulation(5, 1000, 0.8, "sender", 3, 2)


# In[17]:


# common configurations. Please don't change.
servers_number = 5
simulation_time = 1000


# In[18]:


# List of colors used for plotting. Please don't change.
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']


# In[19]:


cache = {}


# In[20]:


def run_experiment(servers_number, simulation_time, utilization, policy, search_limit, queue_threshold):
    if (servers_number, simulation_time, utilization, policy, search_limit, queue_threshold) in cache:
        return cache[(servers_number, simulation_time, utilization, policy, search_limit, queue_threshold)]
    else:
        df = run_simulation(servers_number, simulation_time, utilization, policy, search_limit, queue_threshold)
        cache[(servers_number, simulation_time, utilization, policy, search_limit, queue_threshold)] = df
        return df


# In[21]:


def plot(x, sender_results, receiver_results, utilization, ax0, ax1, color):
    sender_total_messages = []
    receiver_total_messages = []
    sender_cvs = []
    receiver_cvs = []

    for i in range(len(x)):
        df = sender_results[i]
        messages = sum(df['messages'])

        sender_total_messages.append(messages)
        #cv = cv_func(df['queue_length'])
        sender_cvs.append(df['migrations'].sum())

        df = receiver_results[i]
        messages = sum(df['messages'])

        receiver_total_messages.append(messages)
        #cv = cv_func(df['queue_length'].sum())
        receiver_cvs.append(df['migrations'].sum())
    
    if utilization is None:
        sender_label = 'Sender-initiated'
        receiver_label = 'Receiver-initiated'
    else:
        sender_label = f'Sender-initiated, u = {utilization}'
        receiver_label = f'Receiver-initiated, u = {utilization}'
    
    ax0.plot(x, sender_total_messages, label=sender_label, color=color, linestyle='solid')
    ax0.plot(x, receiver_total_messages, label=receiver_label, color=color, linestyle='dashed')

    ax1.plot(x, sender_cvs, label=sender_label, color=color, linestyle='solid')
    ax1.plot(x, receiver_cvs, label=receiver_label, color=color, linestyle='dashed')


# In[22]:


sender_utilization_results = []
receiver_utilization_results = []

#################################
# Configurations
utilizations = [0.1, 0.2,0.3,0.4,0.5,0.6, 0.7, 0.8, 0.9,  0.99]
search_limit = 5
queue_threshold = 1
#################################

total_experiments = len(utilizations)
exp = 1
for utilization in utilizations:
    print(f'Experiment {exp} of {total_experiments}, utilization ratio: {utilization:.1f}')
    df = run_experiment(servers_number=servers_number, simulation_time=simulation_time, utilization=utilization,
                             policy="sender", search_limit=search_limit, queue_threshold=queue_threshold)
    sender_utilization_results.append(df)
    
    df = run_experiment(servers_number=servers_number, simulation_time=simulation_time, utilization=utilization,
                             policy="receiver", search_limit=search_limit, queue_threshold=queue_threshold)
    receiver_utilization_results.append(df)
    
    exp += 1


# In[23]:


fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(15, 5))
plot(utilizations, sender_utilization_results, receiver_utilization_results,
     None, ax0, ax1, 'tab:blue')
ax0.set_xlabel('Utilization Ratio')
ax0.set_ylabel('Total Messages')
ax0.legend()

ax1.set_xlabel('Utilization Ratio')
ax1.set_ylabel('Total Migrations')
ax1.legend()


# # Part 1 Questions.
# 
# What is the effect of increasing the utilization ratio from 0 to 1 on the total number of messages across the cluster? Why?
# 
# Ans) In the sender-initiated policy, the sender will attempt to send messages more often when the usage ratio rises in order to maintain a specific level of network load. As a result, additional messages are transmitted throughout the cluster, increasing the overall amount of messages.
# 
# Increasing the usage ratio in the receiver-initiated policy allows the receiver to process more incoming messages at once. Senders will be able to transmit messages in larger batches and more often as a result, which will increase the overall quantity of messages sent throughout the cluster.
# 
# 
# What is the effect of increasing the utilization ratio from 0 to 1 on the total migrations across the cluster? Why?
# 
# Ans) The number of migrations throughout the cluster tends to increase along with the utilization ratio for sender-initiated rules. This is due to the fact that in sender-initiated policies, it is up to the sender node to choose when to move a job to a less busy node. The overall number of migrations across the cluster rises as the utilization ratio rises because the sender node is more likely to locate a less busy node and migrate work there as a result.
# 
# On the other side, as the utilization ratio rises for receiver-initiated policies, fewer migrations likely to occur across the cluster. When a task from a busy node should be requested under receiver-initiated policies, the receiver node makes the decision. As the utilization ratio increases, the receiver node is more likely to find a busy node, and therefore less likely to request a task, resulting in a decrease in total migrations across the cluster. However, if the utilization ratio becomes too high, the number of migrations may start to increase again as nodes become overwhelmed and begin to offload tasks to other nodes.

# In[25]:


sender_qt_results = {}
receiver_qt_results = {}
#################################
# Test with different values and see the effect in behavior
utilizations = [0.1, 0.2,0.3,0.4,0.5,0.6, 0.7, 0.8, 0.9, 0.97]    #  <- fill in with utilization values (try not giving more than 10 values)
thresholds =   [1,2,3]    #  <- fill in with queue threshold values
search_limit =  5    #  <- fill in with an integer value for search limit
#################################

total_experiments = len(utilizations) * len(thresholds)
exp = 1
for utilization in utilizations:
    sender_qt_results[utilization] = []
    receiver_qt_results[utilization] = []
    for threshold in thresholds:
        print(f'Experiment {exp} of {total_experiments}, queue threshold: {threshold}, '
              f'utilization ratio: {utilization}')
        df = run_experiment(servers_number=servers_number, simulation_time=simulation_time, utilization=utilization,
                                 policy="sender", search_limit=search_limit, queue_threshold=threshold)
        sender_qt_results[utilization].append(df)

        df = run_experiment(servers_number=servers_number, simulation_time=simulation_time, utilization=utilization,
                                 policy="receiver", search_limit=search_limit, queue_threshold=threshold)
        receiver_qt_results[utilization].append(df)
        
        exp += 1


# In[26]:


# You don't need to change this part
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(15, 5))
colors_slice = colors[0:len(utilizations)]#['tab:blue', 'tab:orange', 'tab:green']
for i in range(len(utilizations)):
    plot(thresholds, sender_qt_results[utilizations[i]], receiver_qt_results[utilizations[i]],
         utilizations[i], ax0, ax1, colors_slice[i])
    
ax0.set_xlabel('Queue Threshold')
ax0.set_ylabel('Total Messages')
ax0.legend()

ax1.set_xlabel('Queue Threshold')
ax1.set_ylabel('Total Migrations')
ax1.legend()


# # Part 2 Questions
# 
# What is the effect of increasing the queue threshold from 0 upwards on the total number of messages across the cluster? Why?
# 
# Ans) For both sender-initiated and receiver-initiated policies, increasing the queue threshold from 0 upwards will initially have no effect on the total number of messages across the cluster, as long as the queues are not filled up to the threshold limit. However, once the queues start filling up and reach the threshold limit, the total number of messages across the cluster will start to increase. This is because when the queues are filled up to the threshold limit, any new messages that arrive will be blocked and will not be processed until there is room in the queue. As a result, the sender or receiver will keep retrying to send or receive the blocked messages, leading to an increase in the total number of messages across the cluster.
# 
# 
# What is the effect of increasing the queue threshold from 0 upwards on the total migrations across the cluster? Why?
# 
# And) In the case of sender-initiated policy, increasing the queue threshold can lead to an increase in the total number of migrations across the cluster. This is because when the sender node reaches the threshold, it will start sending messages to other nodes to reduce its queue size, which in turn may cause those nodes to migrate some of their messages to other nodes, leading to additional migrations.
# 
# On the other hand, in the case of receiver-initiated policy, increasing the queue threshold may not have a significant effect on the total number of migrations across the cluster. This is because the receiver nodes are responsible for initiating migrations and they will only do so when their own queues reach a certain threshold. However, if the threshold is set too high, it may lead to increased message latency and potential performance issues.

# In[27]:


sender_sl_results = {}
receiver_sl_results = {}
#################################
# Test with different values and see the effect in behavior
utilizations = [0.1, 0.2,0.3,0.4,0.5,0.6, 0.7, 0.8, 0.96]    #  <- fill in with utilization values (try not giving more than 10 values)
search_limits = [1, 2, 3]   #  <- fill in with search limit values
queue_threshold =  1  #  <- fill with an integer for queue threshold
#################################

total_experiments = len(utilizations) * len(thresholds)
exp = 1
for utilization in utilizations:
    sender_sl_results[utilization] = []
    receiver_sl_results[utilization] = []
    for limit in search_limits:
        print(f'Experiment {exp} of {total_experiments}, search limit: {limit}, '
              f'utilization ratio: {utilization}')
        df = run_experiment(servers_number=servers_number, simulation_time=simulation_time, utilization=utilization,
                                 policy="sender", search_limit=limit, queue_threshold=queue_threshold)
        sender_sl_results[utilization].append(df)

        df = run_experiment(servers_number=servers_number, simulation_time=simulation_time, utilization=utilization,
                                 policy="receiver", search_limit=limit, queue_threshold=queue_threshold)
        receiver_sl_results[utilization].append(df)
        
        exp += 1


# In[28]:


# You don't need to change this part
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(15, 5))
colors_slice = colors[0:len(utilizations)]
for i in range(len(utilizations)):
    plot(search_limits, sender_sl_results[utilizations[i]], receiver_sl_results[utilizations[i]],
         utilizations[i], ax0, ax1, colors_slice[i])
    
    ax0.set_xlabel('Search Limit')
    ax0.set_ylabel('Total Messages')
    ax0.legend()
    
    ax1.set_xlabel('Search Limit')
    ax1.set_ylabel('Search Migrations')
    ax1.legend()


# # Part 3 Questions
# 
# What is the effect of increasing the search limit from 1 upwards on the total number of messages across the cluster? Why?
# 
# Ans) For sender-initiated policies, increasing the search limit can lead to an increase in the number of messages as senders continue to search for the best route to deliver the message. For receiver-initiated policies, increasing the search limit can lead to an increase in the number of messages as receivers broadcast their availability to a wider range of nodes, potentially leading to more migrations.
# 
# However, the effect of increasing the search limit on the total number of messages across the cluster is not always straightforward and can depend on various factors, such as the size of the network, the distribution of nodes, and the routing algorithm used. Therefore, it is important to carefully consider the impact of increasing the search limit before making any changes.
# 
# In receiver-initiated content-based routing, the receiver is responsible for selecting the appropriate messages from the messages that are sent to it based on the message content. The search limit determines how many intermediate nodes the receiver will request to find the appropriate messages. Increasing the search limit from 1 upwards will result in an increase in the total number of messages across the cluster. This is because the receiver will need to send requests to multiple intermediate nodes to find the appropriate messages. Each intermediate node will need to process the request and forward it to the next node in the search path, resulting in an increase in the number of messages across the cluster.
# 
# What is the effect of increasing the search limit from 1 upwards on total migrations across the cluster? Why?
# 
# Ans) In the case of the sender-initiated policy, increasing the search limit can potentially increase the total number of migrations across the cluster. This is because, with a higher search limit, the sender node will have a larger pool of possible candidate nodes to migrate its messages to, increasing the likelihood of finding a suitable destination. However, this can also result in more migrations being initiated, as the sender node will continue searching for a destination until it finds one that satisfies the search criteria.
# 
# On the other hand, in the case of the receiver-initiated policy, increasing the search limit may not have a significant effect on the total migrations across the cluster. This is because, in this policy, it is the receiver node that searches for suitable messages to migrate, based on its own load and capacity. As such, increasing the search limit may not necessarily result in more migrations, as the receiver node may already be handling its workload effectively and may not need to migrate additional messages. However, if the workload on the receiver node increases, a higher search limit may help it identify more candidate messages to migrate, potentially resulting in more migrations across the cluster.

# In[ ]:





# In[ ]:




