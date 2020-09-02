# Geocent DevOps Code Challenge

## The Challenge

#### Part 1
The development teams on your project have been working on a set of microservices. They need your help to "Dockerize" their microservices, datastores, and dependent services. Your goal is to provide each microservice with working Dockerfile(s) and Docker-compose file(s) to deploy the suite of services locally for testing. If all services are configured correctly the `webapp` should look like the image below when rendered.

#### Part 2
In addition, the team would like to use Kubernetes to deploy these services in continuous integration and production environments. Because `Docker for Mac` and `Docker for Windows` provides Kubernetes out-of-the-box, the team would like to be able to test their services locally in Kubernetes before progressing to CI pipelines. Your goal is to prepare Kubernetes configuration in order to deploy the services in a local Kubernetes cluster. If all services are configured correctly the `webapp` should look like the image below when rendered.

![Ideal Scenario image](./ideal-scenario.png)

## Pre-Requisites
- `docker-for-mac` or `docker-for-windows`
	- Includes `docker`, `docker-compose`, `kubectl`, and `kubernetes`

## Provided Architecture
<pre>																			  
                                   counter-service --> redis												
                                  /
Web Browser Client --> nginx-proxy ---- webapp
                                  \
                                   person-service --> postgres
</pre>

## Service Details
- `postgres` - Postgres database used by the `person-service`
	- Base Docker hub image tag: `postgres:11`
	- Exposed port: `5432`
- `redis` - Redis key-value datastore used by the `counter-service`
	- Base Docker hub image tag: `redis:alpine`
	- Exposed port: `6379`
- `person-service` - A spring-boot/Java backend microservice that provides `persons` REST endpoints
	- Base Docker hub image tags: `gradle:5.4-jdk11` and `openjdk:11.0-jdk` (Use multi-stage Dockerfiles)
	- Exposed port: `8080`
- `counter-service` - A Flask/Python backend microservice that provides a `counter` REST endpoint
	- Base Docker hub image tag: `python:3.7`
	- Exposed port: `5000`
- `webapp` - React SPA frontend that consumes the `person-service` and `counter-service`
	- Base Docker hub image tags: `node:12-alpine` and `nginx:1.14.2` (Use multi-stage Dockerfiles)
	- Exposed port: `3000` and/or `80`
- `nginx-proxy` - Proxies to `webapp`, `counter-service`, and `person-service` - Route and proxy all service endpoints through Nginx as a service that is accessible to the host
	- Base Docker hub image tag: `nginx:1.14.2`
	- Exposed port in docker-compose: `8000` and/or `80`
	- Exposed port in Kubernetes: `30500` (Use `NodePort` in the service)

## Part 1 - More Information and Requirements
- Use `docker` - create `Dockerfiles` for each service that needs one.
- Use `docker-compose` stack(s) to network all services according to the architecture above.
- A starter `docker-compose.yml` has been provided with the `postgres` and `redis` services configured. Add the rest of the services to the stack.
- The `.env-dev` has been provided with the necessary environment variables that will be needed by the services.
- The `pull-required-images.sh` script has been provided as a convenience to pull all of the required docker images for this code challenge.

## Part 2 - More Information and Requirements
- Utilize your work from part 1 - i.e. the `Dockerfiles` you prepared.
- Use `kubernetes`
	- You may use `Docker for Mac` Kubernetes, `Docker for Windows` Kubernetes, or `minikube`
	- For deployment tools, you may use `vanilla Kubernetes yaml`, `Helm`, `Kustomize`, or any other tool/scripting that you are comfortable with.

## Solution

#### Part 1 Walkthrough
I have created Dockerfiles for each microservice and placed them under their respective directories. My Dockerfiles contain instructions to pull base images from DockerHub, copy any application src code onto the image if applicable, build any application(s) if applicable, and run any executable(s) if applicable. I have subsequently created a docker-compose.yml file which references the path(s) to each Dockerfile and deploys the images as a functioning suite of microservice containers.

**Steps to replicate and verify it works:**

1. Install `docker-for-mac` or `docker-for-windows` on a local machine
2. Clone this github repo
```
git clone https://github.com/pchen2145/geocent-devops-code-challenge-chen.git
```
3. Change into the project directory and run docker-compose up
```
cd geocent-devops-code-challenge-chen
docker-compose up
```
4. Verify the application is up and running by opening a browser and navigating to `http://localhost:8000`. Hit refresh to see that the hit counter increments each time.

![Local deployment using docker-compose](./screenshot-local-deployment.png)

5. To prepare for Part 2 below, all images were tagged during build and pushed to my personal Dockerhub repo. This allows for a convenient place to pull down custom built images for deployment into Kubernetes in Part 2 of this challenge.
```
docker build ./nginx -t pchen2145/geocent-nginx:v1
docker build ./counter-service -t pchen2145/geocent-countersvc:v1
docker build ./person-service -t pchen2145/geocent-personsvc:v1
docker build ./redis -t pchen2145/geocent-redis:v1
docker build ./postgres -t pchen2145/geocent-postgres:v1
docker build ./webapp -t pchen2145/geocent-webapp:v1

docker push pchen2145/geocent-nginx:v1
docker push pchen2145/geocent-countersvc:v1
docker push pchen2145/geocent-personsvc:v1
docker push pchen2145/geocent-redis:v1
docker push pchen2145/geocent-postgres:v1
docker push pchen2145/geocent-webapp:v1
```

**Notes:**
* I modified line 21 of dev.conf and changed the port number from 3000 to 80 as the nginx.conf file uploaded to the webapp is configured to listen on port 80 by default.

#### Part 2 Walkthrough
Now that we've verified that the suite of services works in a local Docker environment, let's test our deployment of the application into a Kubernetes cluster. Deploying into a Kubernetes cluster adds some complexity, as we have to create additional objects aside from pods such as service objects, deployment objects, and configmap objects. Networking is slightly different compared to Part 1 as pods communicate with each other using a service layer. I've created service objects with ClusterIPs for each service, except for the Nginx proxy which has a service type of NodePort to expose a port on the VM the cluster is running on so external traffic can hit the Nginx proxy.

![Kubernetes Deployment Architecture](./geocent-app-diagram.jpg)

**Steps to replicate and verify it works:**

1. Run steps 1-2 listed in Part 1 above
2. Install a hypervisor onto your local machine. I chose VirtualBox because it was already installed on my machine.
```
brew update
brew tap caskroom/cask
brew search virtualbox
brew cask install virtualbox
brew cleanup
```
3. Install minikube on a local machine (macOS)
```
brew install minikube
```
4. Once installed, start a single node kubernetes cluster inside a VirtualBox VM
```
minikube start
```
5. Verify the cluster is up and ready. The command below also reveals the IP address of the VM.
```
minikube status
```
6. To simplify our deployment and bundle everything nicely in an organized fashion, let's install Helm and use it to deploy
```
brew install kubernetes-helm
helm init
```
7. To deploy the set of microservices to the minikube cluster, make sure you are inside the cloned project directory and run
```
helm install app ./k8sdeployment/app
```
8. This step might take a few minutes as images will need to be pulled down and deployed. Check the status of the deployment by running
```
kubectl get pods
kubectl get deployments
```
9. Due to the fact that `localhost` has been hardcoded into some of the application's REST endpoints, we need to map our local machine's port 30500 to the IP and port 30500 of the VM in order for our webapp application to retrieve data from the person-service and counter-service microservices.
```
ssh -i $(minikube ssh-key) docker@$(minikube ip) -L 30500:localhost:30500
```
10. Navigate to `http://localhost:30500` using a browser to verify that the application is up and running. Hit refresh to see that the hit counter increments each time.

![Kubernetes deployment using Helm](./screenshot-k8s-deployment.png)

#### Cleaning up
11. Helm makes it easy to delete deployments. To delete the deployment run
```
helm delete app
```
12. To terminate the minikube cluster and VM, run
```
minikube delete
```
**Notes:** 
* The variables in the .env-dev file can no longer be passed into the container environment using the method in Part 1. A configMap object was created instead to store these values and provide them to the containers at runtime. 
* A secrets object could be used as well to pass sensitive information to containers at runtime.
* In this example, I loaded the kubernetes.conf file into the webapp server via a mounted volume and configMap. I noticed the upstream hostname was changed from webapp to webapp-service within the file so I modified my webappService.yaml file to reflect this new hostname.
* Each service has been defined as deployment containing a replicaset. If a pod is forced to terminate or is killed, the controller will automatically try to spin up a replacement.
