Title: A Quick Intro to Kubernetes
Date: 2018-02-01
Category: k8s, dev, h4x0r

![cyberpunk](./cyberpunk/27.jpg){:height="300px" width="400px"}


Wanna try Kubernetes for the first time and don't know how to start? No problem! I wrote this quick guide to help some of the junior engineers in my team at Etsy to get started with k8s!

In this guide I will show you how to spin a quick Node.js server in kubernetes and to grasp some of its main concepts. Read on! [Here is the source code](https://github.com/bt3gl/k8s_security).

### Install kubectl

First things first, you will need to install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in your machine or VM.

Make sure you have all the auths right:

1. Create a auth token and move to `~/.kube`
2. Create a config file and move to `~/.kube`


### Spinning up a Hello World node server in docker

Download [this code](https://github.com/bt3gl/intro_to_k8s/tree/master/node_server_example) and build the image:

```
$ make build:
```

Now, just run the container:

```
$ make run
```

Which is:
```
docker build -t  node_app_test .
```

Check whether the server is up:
```
$ make curl
```

```
$ make status
```


#### Other useful commands

Exec inside the container:

```
$ docker exec -i -t <container name from status> /bin/bash
```

Check images in disk:

```
$ docker images
```


### Pushing the Registry to Kubernetes

In a real production system, we’ll want to build images in one place, then run them in the Kubernetes cluster. The system that
 stores these images for distribution out to the running containers is called a **container registry**.


Using a `yaml` Kubernetes files (for example, the one inside `node_server_example/` you can now deploy the image with

```
$ kubectl create -f  node_example_kube_config.yaml
```

Now you can create the service with:

```
$  kubectl expose deployment node-app-test
```
See the service at:

```
$ kubectl get services
```

### Clean up

Removing the service and the deployment when you are done:

```
$ kubectl delete service node-app-test
$ kubectl delete deployment node-app-test
```



## Useful General Commands

Checking out pods:

```
$ kubectl get pods --namespace=security
```

Checking deployments:

```
$ kubectl get deployments --namespace=security
```

Checking services:

```
$ kubectl get services --namespace=security
```

Get more information about a pod:

```
$ kubectl describe pod --namespace=security <pod name>
```



## Some References:

* [Dockerfiles good practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#general-guidelines-and-recommendations).

----
***Thank you for reading, and let me know what you think!***
