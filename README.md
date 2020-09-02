# Helm Demo

What is Helm? Simply put, Helm is a deployment package manager for Kubernetes.

Helm lets you create, organize, and publish releases for Kubernetes objects, using a powerful templating framework that can dynamically generate Kubernetes manifests and apply them.

Think of Helm as a tool that can bundle multiple components of your release package, and allow you to deploy them together as one cohesive unit which can be versioned.

In this demo, I have an application consisting of 6 components (React front-end, Python application, Java Springboot microservice, Nginx webserver, Redis data layer, and Postgres database). These 6 components are all tied together and ideally should be deployed into production as a single packaged "unit". Helm allows us to achieve this goal and also gives us the flexibility to upgrade releases, rollback releases, and also allow users to define configuration/specification values that feed into the deployed release.

