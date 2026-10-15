# Practical 1 --- Smart City Air-Quality Monitoring with Kubernetes Microservices

## Aim

Deploy a browser frontend and two Flask microservices to Kubernetes,
then verify internal service discovery through Kubernetes DNS.

## Problem Statement

A city monitoring portal retrieves air-quality readings from an internal
data-provider service through an aggregator. The browser frontend calls
the aggregator through Nginx. The aggregator contacts the data provider
using its Kubernetes Service name rather than a Pod IP.

> **Note:** The values shown are mock demonstration data, not live
> air-quality measurements.

## Architecture

``` text
Browser
  |
  v
Nginx Frontend (NodePort)
  |
  | /api/reading
  v
air-gateway-svc:5000 (ClusterIP)
  |
  | http://air-data-svc:5000/reading
  v
air-data-svc:5000 (ClusterIP)
  |
  v
JSON air-quality reading
```

## Requirements

-   Docker Desktop
-   Minikube
-   kubectl
-   Visual Studio Code
-   The complete `practical1-air-quality` project folder

No source-code edits are required when using the supplied project files
and this guide.

## Run the Practical

Run all commands from the `practical1-air-quality` folder in the VS Code
terminal.

### 1. Start Docker Desktop and Kubernetes

Open Docker Desktop and wait until its engine is running. Then execute:

``` bash
minikube start --driver=docker
```

Verify the cluster:

``` bash
minikube status
kubectl get nodes
```

Continue when Minikube components are running and the `minikube` node
shows `Ready`.

### 2. Build the application images

Run these commands exactly as shown:

``` bash
docker build -t air-data:v1 ./data-service
docker build -t air-gateway:v1 ./gateway
docker build -t air-frontend:v2 ./frontend
```

The frontend image uses the already-configured `air-frontend:v2` tag for
the updated dashboard.

### 3. Load images into Minikube

``` bash
minikube image load air-data:v1
minikube image load air-gateway:v1
minikube image load air-frontend:v2
```

### 4. Deploy the application

``` bash
kubectl apply -f k8s.yaml
```

Wait for the Deployments to become available:

``` bash
kubectl rollout status deployment/air-data
kubectl rollout status deployment/air-gateway
kubectl rollout status deployment/air-frontend
```

Check the resources:

``` bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Wait until the three application Pods show `1/1 Running`.

### 5. Open the interactive dashboard

Run:

``` bash
minikube service air-frontend-svc --url
```

Open the URL printed by Minikube in your browser. If Minikube says the
command or tunnel must remain running, keep that terminal open while
using the application.

Click **Fetch air-quality reading** on the dashboard. The frontend sends
a request to `/api/reading` and displays the response from the backend
services.

Example response shape:

``` json
{
  "gateway": "air-quality-aggregator",
  "service_discovery": "success",
  "reading": {
    "station": "Central Ward",
    "pm25_ug_m3": 34,
    "pm10_ug_m3": 61,
    "aqi_category": "Moderate",
    "source": "Demo sensor payload"
  }
}
```

The actual values depend on the mock payload configured in the project.

### 6. Verify Kubernetes DNS service discovery

Open a second VS Code terminal in the project folder and find the
gateway Pod:

``` bash
kubectl get pods -l app=air-gateway
```

Copy the Pod name shown. Then run the following command, replacing
`<GATEWAY_POD_NAME>` with the actual name:

``` bash
kubectl exec -it <GATEWAY_POD_NAME> -- python -c "from urllib.request import urlopen; print(urlopen('http://air-data-svc:5000/reading').read().decode())"
```

A JSON reading confirms that the gateway Pod can resolve `air-data-svc`
using Kubernetes DNS and reach the data provider through its Service
name.

You can also inspect the service endpoints:

``` bash
kubectl get endpoints air-data-svc air-gateway-svc
```

## Troubleshooting

### Minikube or Kubernetes is unreachable

Make sure Docker Desktop is running, then execute:

``` bash
minikube start --driver=docker
minikube status
kubectl get nodes
```

### A Pod is not running

``` bash
kubectl get pods
kubectl describe pods
kubectl logs deployment/air-data
kubectl logs deployment/air-gateway
kubectl logs deployment/air-frontend
```

### The dashboard opens but cannot fetch a reading

``` bash
kubectl get endpoints air-data-svc air-gateway-svc
kubectl logs deployment/air-gateway
kubectl logs deployment/air-data
```

### The old frontend appears

The supplied Kubernetes manifest and image tag are intended to run the
updated frontend without manual code changes. If an older image was
already running in a previous setup, confirm the running frontend
Deployment is using the project's configured `air-frontend:v2` image.
Rebuild/load steps are listed above; no source-code editing is required.

## Stop the Practical

To remove the application resources and stop Kubernetes:

``` bash
kubectl delete -f k8s.yaml
minikube stop
```

## Conclusion

This practical demonstrates Nginx reverse proxying, independent Flask
microservices, Docker images, Kubernetes Deployments, ClusterIP and
NodePort Services, and service discovery using Kubernetes DNS. The
browser dashboard makes the air-quality response interactive, while
Kubernetes commands verify the deployment and internal communication.
