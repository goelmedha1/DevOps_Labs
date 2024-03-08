[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/gWcEmUvr)


Compsci 677: Distributed and Operating Systems
​
Spring 2023
​
# Homework 7: Minikube
​
The purpose of this homework is to provide hands-on experience with kubernetes using minikube, a local kuberenetes environment which focuses on making it easy to learn and develop for Kubernetes.
​
## Installing Minikube
Follow the instructions present [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/) to install minikube. It supports all major platforms (Linux, macOS, and Windows). This homework is based on the simple getting started minikube instructions on this page.
​
## Start Minikube Cluster
Make sure that docker is running before starting minikube
```shell
minikube start
```
If minikube fails to start, see the [drivers page](https://minikube.sigs.k8s.io/docs/drivers/) for help setting up a compatible container or virtual-machine manager. If there are still issues encountered in minikube start, try searching for the errors online and try to resolve them on your own by looking at similar github issues. If everything installs correctly you should be able to see the docker container for minikube up and running.
```shell
docker ps | grep minikube
```
​
## Interact with Cluster
If you already have kubectl installed,it can be installed from [here](https://kubernetes.io/docs/tasks/tools/), you can now use it to access your shiny new cluster:
```shell
kubectl get po -A
```

Alternatively, minikube can download the appropriate version of kubectl and you should be able to use it like this:
```shell
minikube kubectl -- get po -A
```
You can also make your life easier by adding the following to your shell config:
```shell
alias kubectl="minikube kubectl --"
```
​
Initially, some services such as the storage-provisioner, may not yet be in a Running state. This is a normal condition during cluster bring-up, and will resolve itself momentarily. For additional insight into your cluster state, minikube bundles the Kubernetes Dashboard, allowing you to get easily acclimated to your new environment:
​
```shell
minikube dashboard
```
If minikube dashboard command is stuck verifying proxy health, delete the cluster and start it again
```shell
minikube delete --all
minikube start
minikube dashboard
```
​
## Basic Deployments
Create a sample deployment and expose it on port 8080:
```shell
kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
kubectl expose deployment hello-minikube --type=NodePort --port=8080
```
It may take a moment, but your deployment will soon show up when you run:
```shell
kubectl get services hello-minikube
```
The easiest way to access this service is to let minikube launch a web browser for you (this works only for linux deployments):
```shell
minikube service hello-minikube
```
Alternatively, use kubectl to forward the port:
```shell
kubectl port-forward service/hello-minikube 7080:8080
```
Tada! Your application is now available at http://localhost:7080/.
​

You should be able to see the request metadata from nginx such as the CLIENT VALUES, SERVER VALUES, HEADERS RECEIVED and the BODY in the application output. Try changing the path of the request and observe the changes in the CLIENT VALUES. Similarly, you can do a POST request to the same and observe the body show up in BODY section of the output.

### Listing Objects
K8s allow listing different types of objects. For example. Listing shows the objects and the state of each kind.

```
kubectl get pods # List Pods
kubectl get services # List services
kubectl get deployment # List deployment
```

### Describe Objects
Describe is an important debugging tool, that shows the state, history, and details of a k8s object.

```
kubectl describe pod hello-minikube
Name:             hello-minikube-fdf664d87-mtn29
...
```
Same goes for `deployment` and `services`.

### Delete Objects
You can delete the object by specifying its type and name.
```
kubectl delete deployment hello-minikube
deployment.apps "hello-minikube" deleted
```

## Real-Application Deployment
In the previous section, we introduced simple methods to deploy an an application. In the previous parts we used two k8s object deployment and service. However, we didn't define them. 


A Kubernetes **deployment** is a grouping method of pods, where they can be created/updated/delete together. Once you have defined and deployed your deployment Kubernetes will then work to make sure all pods managed by the deployment meet whatever requirements you have set.  On the other hand **service** is a way to expose a pod to the internal/external world via a fixed name. Deployments and Services are often used in tandem: Deployments working to define the desired state of the application and Services working to make sure communication between almost any kind of resource and the rest of the cluster is stable and adaptable.


### Deploying a Custom Application
The folder `simple-app` contains a simple application that return a random number of things. Similar to last time we can create a deployment as shown below. 
```
kubectl create deployment simple-app --image=washraf/simple-app
kubectl expose deployment simple-app --type=NodePort --port=80
kubectl port-forward service/simple-app 8080:80
```
Open the browser `http://127.0.0.1:8080/` you will find the web application open.

> Note: We provided a built version of the container, you can replace this with your own.

However, this method is not the best method for managing k8s objects. K8s supports three object management methods, the previous method is called 
`Imperative commands` and should be in development environments. However, the `Imperative object configuration` and `Declarative object configuration` are made for production and automation usage. 
> Note: The detailed comparison is available [here](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/).

Lets redeploy the application using `Declarative object configuration`, we used this mode as its more general.

```
$ kubectl apply -f simple-app/deploy.yaml
service/simple-app-svc created
deployment.apps/simple-app created
$ kubectl port-forward service/simple-app 8080:80
```
> Note: If you are reusing the ports, make sure they are not used.


List Pods:
```
$ kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
simple-app-5b566cf475-sfkc2   1/1     Running   0          16s
```
List Deployment
```
$ kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
simple-app   1/1     1            1           24s
```
List Services
```
$ kubectl get service
NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP        149m
simple-app-svc   ClusterIP   10.101.140.244   <none>        80/TCP         31s
```
The `deploy.yaml` file has two main sections:
Service Section (top) and Deployment Section (bottom).
The deployment section describe the used pods in the spec section by describing the containers' images, and ports. THe service section describe the port mapping.

You can delete the deployment and service using 
```
$ kubectl delete -f simple-app/deploy.yaml
service "simple-app-svc" deleted
deployment.apps "simple-app" deleted
```



## Manage your cluster
Pause Kubernetes without impacting deployed applications:
```shell
minikube pause
```
Unpause a paused instance:
```shell
minikube unpause
```
Halt the cluster:
```shell
minikube stop
```
Increase the default memory limit (requires a restart):
```shell
minikube config set memory 16384
```
Browse the catalog of easily installed Kubernetes services:
```shell
minikube addons list
```
Create a second cluster running an older Kubernetes release:
```shell
minikube start -p aged --kubernetes-version=v1.16.1
```
Delete all of the minikube clusters:
```shell
minikube delete --all
```
  
### What to submit
  
Submit a brief report explaining whether you could complete all the steps, output of the commands shown above and a screenshots of the dashboard and the application. List any issues you faced, if any.   
