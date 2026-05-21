# Employee Management API is a lightweight Flask-based REST API

# Docker Part

## Project Structure
```bash
employee-api/
│
├── app.py
├── requirements.txt
└── Dockerfile
```
## Build Docker image 

```bash
docker build -t thej-api-image .

docker run -d -p 5000:5000 thej-api-image 

docker ps 
```

## Test App Locally

- Root Endpoint curl http://localhost:5000/
- Employees Endpoint curl http://localhost:5000/employees
- Health Endpoint curl http://localhost:5000/health
- Info Endpoint curl http://localhost:5000/info

# Minikube Part 

```bash
minikube start 

minikube start --memory=4096 --cpus=2

kubectl get nodes

eval $(minikube docker-env)

docker build -t thej-api-image:latest ./app

```

## Enable Minikube Addons

```bash
minikube addons enable ingress

minikube addons enable metrics-server

minikube addons list

```


# K8s Part 


```bash
k8s/
│
├── 01-namespace.yml
├── 02-configmap.yaml
├── 03-deployment.yaml
├── 04-service.yaml
├── 05-ingress.yaml
└── 06-hpa.yaml
```

## create 

```bash
kubectl apply -f k8s/ 
```

## Output

```bash
➜  k8s kubectl apply -f .
namespace/employee-ns created
configmap/employee-api-config created
deployment.apps/employee-api-deployment created
service/employee-api-service created
ingress.networking.k8s.io/employee-api-ingress created
horizontalpodautoscaler.autoscaling/employee-api-hpa created
➜  k8s
```

## Test App 

```bash
minikube ip 
# output: 192.168.49.2
```
- Update into /etc/hosts file 

```bash
192.168.49.2 employee.local
```

## Test App inside k8s output 

```bash
➜  k8s curl http://employee.local
{"application":"Employee Management API","environment":"development","hostname":"employee-api-deployment-576458f995-8x4d5","message":"Application is running successfully"}
# /health
➜  k8s curl http://employee.local/health
{"status":"UP"}
# /info
➜  k8s curl http://employee.local/info
{"deployment_time":"2026-05-20 08:28:55.207011","environment_name":"development","hostname":"employee-api-deployment-576458f995-hjbvr","platform_team":"platform-engineering","version":"v1"}
# /Employees 
➜  k8s curl http://employee.local/employees
{"employees":[{"department":"DevOps","employee_id":101,"employee_name":"Rahul Sharma"},{"department":"Platform Engineering","employee_id":102,"employee_name":"Anjali Verma"},{"department":"Cloud Operations","employee_id":103,"employee_name":"Kiran Kumar"}]}
➜  k8s
```

## Increase Load 

```bash
kubectl run -i --tty load-generator \
--rm --image=busybox \
-n employee-ns -- /bin/sh
```

Inside pod run:

```bash
while true; do wget -q -O- http://employee-api-service; done
```

To watch HPA scaling:

```bash
kubectl get hpa -n employee-ns -w
```

To watch pods scaling:

```bash
kubectl get pods -n employee-ns -w
```





# Helm Part 

# Helm Golden Path Implementation — Employee API Project

## Prerequisites

Before starting, make sure:

* Minikube is running
* Docker image is already built
* Ingress addon enabled
* Metrics server enabled for HPA

Enable addons:

```bash id="p8z7rc"
minikube addons enable ingress
minikube addons enable metrics-server
```

Verify:

```bash id="wzh2xg"
minikube addons list
```

---

# Step 1 — Create Helm Workspace

```bash id="sqv8hb"
mkdir helm
cd helm
```

Create Helm chart:

```bash id="d5lv6q"
helm create golden-app
```

---

# Step 2 — Clean Default Templates

Go inside templates folder:

```bash id="cxqjzm"
cd golden-app/templates
```

Delete default files:

```bash id="i8qv4y"
rm -rf *
```

---

# Step 3 — Create Required Template Files

Create namespace first:

```bash id="f1k7bw"
kubectl create namespace employee-ns
```

Create template files:

```bash id="efj1nv"
touch deployment.yaml
touch service.yaml
touch configmap.yaml
touch ingress.yaml
touch hpa.yaml
```

---

# Step 4 — Final Helm Project Structure

```text id="5d98r4"
golden-app/
│
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-stage.yaml
├── values-prod.yaml
│
├── charts/
│
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── ingress.yaml
    └── hpa.yaml
```

---

# Step 5 — Update Chart.yaml

File:

```text id="2o6xqk"
golden-app/Chart.yaml
```

Example:

```yaml id="c2v8r1"
apiVersion: v2
name: golden-app
description: Helm chart for Employee Management API
type: application
version: 0.1.0
appVersion: "1.0"
```

---

# Step 6 — Create values.yaml

Common default values.

File:

```text id="pcf7g9"
golden-app/values.yaml
```

Contains:

* Image details
* Replica count
* Service configuration
* Ingress configuration
* HPA configuration

---

# Step 7 — Create Environment Values Files

## values-dev.yaml

```text id="q0z5my"
golden-app/values-dev.yaml
```

Dev-specific values:

* Lower replicas
* Dev hostname
* Dev environment variables

---

## values-stage.yaml

```text id="r7g3ld"
golden-app/values-stage.yaml
```

Stage-specific values:

* Moderate replicas
* Stage hostname
* Stage configurations

---

## values-prod.yaml

```text id="k9y2vs"
golden-app/values-prod.yaml
```

Production-specific values:

* Higher replicas
* Production hostname
* Production scaling values

---

# Step 8 — Create ConfigMap Template

File:

```text id="7mgj1v"
templates/configmap.yaml
```

Purpose:

* Store environment variables
* Externalize configurations
* Reusable deployment settings

Example:

* ENVIRONMENT
* PLATFORM_TEAM
* VERSION

---

# Step 9 — Create Service Template

File:

```text id="vvf9x8"
templates/service.yaml
```

Purpose:

* Expose application internally
* Connect pods with networking
* Enable service discovery

Service Type:

```yaml id="7wlx3r"
ClusterIP
```

---

# Step 10 — Create Deployment Template

File:

```text id="t0m3jf"
templates/deployment.yaml
```

Responsibilities:

* Pod creation
* Replica management
* Container image configuration
* Resource allocation
* Health probes

Include:

* Liveness probe
* Readiness probe
* ConfigMap environment injection

---

# Step 11 — Create Ingress Template

File:

```text id="x6qf7n"
templates/ingress.yaml
```

Purpose:

* External access to application
* Domain-based routing
* Reverse proxy support

Example host:

```text id="d9v3wk"
employee.local
```

---

# Step 12 — Create HPA Template

File:

```text id="7qg8rm"
templates/hpa.yaml
```

Purpose:

* Automatic pod scaling
* CPU-based scaling
* Better resource optimization

Requires:

* Metrics server enabled

---

# Step 13 — Validate Helm Chart

Run:

```bash id="x7v2lc"
helm lint golden-app
```

Expected output:

```text id="y3k8dn"
0 chart(s) failed
```

---

# Step 14 — Install Helm Release

```bash id="y8q4ph"
helm install golden-release ./golden-app -n employee-ns
```

Verify resources:

```bash id="g6z3ta"
kubectl get all -n employee-ns
```

---

# Step 15 — Deploy Development Environment

```bash id="c9l5dv"
helm install dev-release ./golden-app \
-f golden-app/values-dev.yaml \
-n employee-ns
```

---

# Step 16 — Deploy Stage Environment

```bash id="r2x6kb"
helm install stage-release ./golden-app \
-f golden-app/values-stage.yaml \
-n employee-ns
```

---

# Step 17 — Deploy Production Environment

```bash id="n4v1qc"
helm install prod-release ./golden-app \
-f golden-app/values-prod.yaml \
-n employee-ns
```

---

# Step 18 — Verify Deployments

Check pods:

```bash id="p4m8jt"
kubectl get pods -n employee-ns
```

Check services:

```bash id="d0y3kq"
kubectl get svc -n employee-ns
```

Check ingress:

```bash id="j8w5lr"
kubectl get ingress -n employee-ns
```

Check HPA:

```bash id="m7c1vb"
kubectl get hpa -n employee-ns
```

---

# Important for Local Minikube Images

If image is locally built:

```yaml id="o7z9tw"
imagePullPolicy: Never
```

Otherwise Kubernetes tries to pull from DockerHub.

---

# Common Helm Commands

## Install Helm

```bash id="q6r3zd"
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

---

## Check Helm Version

```bash id="j9v2nh"
helm version
```

---

## Create Helm Chart

```bash id="b8t6pc"
helm create golden-app
```

---

## Validate Chart

```bash id="w1g9rk"
helm lint golden-app
```

---

## Install Release

```bash id="z3p6vm"
helm install golden-release ./golden-app -n employee-ns
```

---

## Install Using Values File

```bash id="y0f4nd"
helm install dev-release ./golden-app \
-f golden-app/values-dev.yaml \
-n employee-ns
```

---

## Check Releases

```bash id="m4q7zb"
helm list -n employee-ns
```

---

## Check All Releases

```bash id="q8t1cx"
helm list -A
```

---

## Release Status

```bash id="n7k2pw"
helm status golden-release -n employee-ns
```

---

## Upgrade Release

```bash id="j5x8md"
helm upgrade golden-release ./golden-app -n employee-ns
```

---

## Upgrade Using Values File

```bash id="z6v1qt"
helm upgrade golden-release ./golden-app \
-f golden-app/values-prod.yaml \
-n employee-ns
```

---

## Release History

```bash id="w0c5jr"
helm history golden-release -n employee-ns
```

---

## Rollback Release

```bash id="v9p3mk"
helm rollback golden-release 1 -n employee-ns
```

---

## Uninstall Release

```bash id="g2y6ls"
helm uninstall golden-release -n employee-ns
```

---

## Generate Kubernetes YAML

```bash id="u1n7qx"
helm template golden-release ./golden-app
```

---

## Package Helm Chart

```bash id="t5m8kr"
helm package golden-app
```

---

# Real-Time DevOps Understanding

## Why Helm?

Helm helps:

* Reuse Kubernetes manifests
* Manage environments easily
* Simplify upgrades and rollbacks
* Reduce YAML duplication

---

## Why Values Files?

Different environments require different configurations:

| Environment | Example     |
| ----------- | ----------- |
| Dev         | 1 replica   |
| Stage       | 2 replicas  |
| Prod        | 3+ replicas |

Values files make environment management simple.

---

# Interview Tip

In real enterprise projects:

* Helm is the standard Kubernetes package manager
* Separate values files are maintained for Dev, Stage, and Prod
* Helm rollback is heavily used during failed deployments
* HPA and Ingress are common production requirements
