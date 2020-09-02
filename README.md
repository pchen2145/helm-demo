# Helm Demo

What is Helm? Simply put, Helm is a deployment package manager for Kubernetes.

Helm lets you create, organize, and publish releases for Kubernetes objects, using a powerful templating framework that can dynamically generate Kubernetes manifests and apply them.

Think of Helm as a tool that can bundle multiple components of your release package, and allow you to deploy them together as one cohesive unit which can be versioned.

In this demo, I have an application consisting of 6 components (React front-end, Python application, Java Springboot microservice, Nginx webserver, Redis data layer, and Postgres database). These 6 components are all tied together and ideally should be deployed into production as a single packaged "unit". Helm allows us to achieve this goal and also gives us the flexibility to upgrade releases, rollback releases, and also allow users to define configuration/specification values that feed into the deployed release.

Pre Requisites:
- Minikube 1.8.1
- Helm 3.1.1
- Kubectl 1.17.3
- Docker 19.03.8

Note that the docker images for these applications have already been built and have been pushed to my personal Dockerhub repository. This is where the images are pulled from by default, as specified in values.yaml.

Steps:
- Clone this repository
- Start your minikube cluster
- Run `helm install app ./k8sdeployment/app`
- Run the port forward command `ssh -i $(minikube ssh-key) docker@$(minikube ip) -L 30500:localhost:30500`
- Navigate to http://localhost:30500
