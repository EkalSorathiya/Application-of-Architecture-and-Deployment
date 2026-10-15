# Kubernetes Practical Assignments

**Ekal Sorathiya · R014**

This repository contains two hands-on Kubernetes practical projects that
demonstrate how containerized applications are built, deployed, exposed,
and verified in a local Kubernetes environment.

The projects cover two different use cases: a microservices-based
smart-city air-quality dashboard and a machine-learning API for wine
classification.

## Projects

### 1. Smart City Air-Quality Monitoring

**Folder:** `practical1-air-quality`

A web-based monitoring dashboard backed by two Flask microservices. The
Nginx frontend sends requests to an aggregator service, which retrieves
a reading from an internal data-provider service using Kubernetes DNS.

**What it demonstrates** - Interactive browser-based dashboard -
Communication between independent Flask microservices - Nginx reverse
proxying - Kubernetes Deployments and Services - Internal service
discovery through Kubernetes DNS - Containerization with Docker

**Architecture at a glance**

`Browser → Nginx Frontend → Flask Gateway → Flask Data Service → JSON Reading`

The air-quality readings are mock demonstration values, not live sensor
measurements.

### 2. Wine Classification API

**Folder:** `practical2-wine-api`

A machine-learning application that serves wine-classification
predictions through a Flask API. The model is packaged into a Docker
image and deployed to Kubernetes, where its endpoint can be tested and
the deployment can be scaled.

**What it demonstrates** - Machine-learning model training with the
scikit-learn Wine dataset - Flask API for model inference - Docker-based
packaging - Kubernetes Deployment and Service exposure - Prediction
requests and JSON responses - Replica scaling and rolling-update
concepts

## Repository Structure

-   `practical1-air-quality/` --- source files and its own README for
    the air-quality microservices practical
-   `practical2-wine-api/` --- source files and its own README for the
    wine-classification practical
-   `.gitignore` --- files and local artifacts excluded from Git
    tracking
-   `README.md` --- overview of the repository and both projects

## Technologies

**Docker · Kubernetes · Minikube · kubectl · Flask · Nginx · Python ·
scikit-learn**

## Purpose

These projects are intended for practical learning and demonstration.
Together, they show how Kubernetes can support both a multi-service web
application and a containerized machine-learning inference service.

For prerequisites, setup, execution steps, verification, and
troubleshooting, refer to the README inside each practical's folder.
