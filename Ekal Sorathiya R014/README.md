# Two Runnable Kubernetes Practicals (VS Code)

This workspace contains two separate practical projects. Open this folder in VS Code and follow each project's README.

## Practical 1 — Smart City Air-Quality Microservices
Demonstrates Nginx frontend, two Flask services, Kubernetes DNS/service discovery, ClusterIP, NodePort, and browser-to-backend communication.

Folder: `practical1-air-quality/`

## Practical 2 — Wine Classification API on Kubernetes
Demonstrates model training, model serialization, Flask REST API, Docker, Kubernetes Deployment and NodePort, scaling from 2 to 4 replicas, and rolling update from Decision Tree to Random Forest.

Folder: `practical2-wine-api/`

## Prerequisites
- Docker Desktop installed and running
- Minikube installed
- kubectl installed
- Python 3 installed
- VS Code (recommended)

On macOS with the Docker driver, leave the terminal running `minikube service ... --url` open while testing the local URL.

## Suggested workflow
1. Open this folder in VS Code.
2. Open the integrated terminal (`Terminal` → `New Terminal`).
3. Follow the README in Practical 1, then Practical 2.
4. Capture your actual browser and terminal outputs for submission.

The air-quality payload is demo data, not a live sensor feed.


## Interactive demonstration screens
- Practical 1: Open the Minikube URL for `air-frontend-svc` to use the AirAware dashboard and fetch a reading through both Flask microservices.
- Practical 2: Open the base Minikube URL for `wine-model-service` to use the VineIQ dashboard. The form calls the Flask `/predict` endpoint using POST and shows the class result plus raw JSON.
- Browser URLs must be the base service URL, not `/predict`.
