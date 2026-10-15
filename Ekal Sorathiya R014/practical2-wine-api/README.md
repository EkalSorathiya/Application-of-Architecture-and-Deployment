# Practical 2 — Wine Classification API Deployment on Kubernetes

## Aim
Train a machine-learning classifier on the Wine dataset, serve predictions through Flask, package it in Docker, deploy it to Kubernetes, scale replicas, and perform a rolling update.

## Dataset and model
The built-in scikit-learn Wine dataset contains 178 samples, 13 numeric chemical features, and three target classes. The model is a Decision Tree classifier. The API accepts exactly 13 numeric values in the feature order returned by `sklearn.datasets.load_wine()`.

## Requirements
Docker Desktop, Minikube, kubectl, Python 3. Open this folder in VS Code and use its integrated terminal.

## 1. Train the model

```bash
python3 -m pip install -r requirements.txt
python3 train_model.py
```

This creates `wine_model.joblib` and prints the measured test accuracy. Do not copy a guessed accuracy into your report; use the value from your run.

## 2. Build and load the Docker image

```bash
docker build -t wine-classifier:v2 .
minikube start --driver=docker
minikube image load wine-classifier:v2
```

## 3. Deploy to Kubernetes

```bash
kubectl apply -f ml-k8s.yaml
kubectl get pods -l app=wine-model
kubectl get svc wine-model-service
```

Initially, wait for two Pods to show `1/1 Running`. The Service should show NodePort `5000:30510/TCP`.

## 4. Open the API

```bash
minikube service wine-model-service --url
```

Keep this terminal open if Minikube requests it. Open the printed URL in a browser. The root endpoint should return healthy JSON.

## 5. Send a valid prediction request

Use Python to generate a request with an actual Wine dataset row. Run this in a second terminal from this project directory:

```bash
python3 -c "from sklearn.datasets import load_wine; import json; print(json.dumps({'features': load_wine().data[0].tolist()}))"
```

Copy the generated JSON into the following request. Replace `PORT` with the port in the Minikube URL and replace the example array with the generated 13 values:

```bash
curl -X POST http://127.0.0.1:PORT/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[PASTE_13_NUMERIC_VALUES_HERE]}'
```

The API responds with `status`, `prediction_code`, and `predicted_class`. The predicted class depends on the provided feature values and trained model.

## 6. Scale from two replicas to four

```bash
kubectl scale deployment wine-model-deployment --replicas=4
kubectl get pods -l app=wine-model
kubectl get deployment wine-model-deployment
```

Wait until all four Pods are Ready.

## 7. Demonstrate a rolling update

Change `train_model.py` to use Random Forest. Replace the Decision Tree import and model creation with:

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
```

Keep the rest of the training script unchanged. Retrain and build a new image tag:

```bash
python3 train_model.py
docker build -t wine-classifier:v3 .
minikube image load wine-classifier:v3
kubectl set image deployment/wine-model-deployment wine-api=wine-classifier:v3
kubectl rollout status deployment/wine-model-deployment
kubectl get pods -l app=wine-model
```

Expected: rollout completes and the replacement Pods become Ready. Test `/predict` again. The service contract stays the same while the model implementation changes.

## Troubleshooting

```bash
kubectl get pods -l app=wine-model
kubectl describe pod <POD_NAME>
kubectl logs deployment/wine-model-deployment
kubectl get svc wine-model-service
kubectl rollout status deployment/wine-model-deployment
```

To revert a failed rollout:

```bash
kubectl rollout undo deployment/wine-model-deployment
```

## Stop and clean up

```bash
kubectl delete -f ml-k8s.yaml
minikube stop
```

## Conclusion
This practical demonstrates model training and serialization, Flask inference, Docker packaging, Kubernetes Deployment and NodePort, prediction testing, scaling, and rolling update.

## Browser-based prediction UI (updated)

The application now serves a browser form at `/`. Open the base URL printed by `minikube service wine-model-service --url` (do not open `/predict` directly). Enter the 13 values and click **Predict wine class**; the page sends a JSON `POST` request to `/predict` and displays the predicted class plus the raw JSON response. `/health` is the API health endpoint.

### Deploy and open the interactive UI

The current image is `wine-classifier:v2`. From this folder, after Docker Desktop is running and `wine_model.joblib` exists, run:

```bash
docker build -t wine-classifier:v2 .
minikube image load wine-classifier:v2
kubectl apply -f ml-k8s.yaml
kubectl rollout status deployment/wine-model-deployment
kubectl get pods -l app=wine-model
minikube service wine-model-service --url
```

Open the **base URL** printed by Minikube (for example `http://127.0.0.1:56354/`). The VineIQ dashboard shows a live API status badge, 13 editable inputs, sample/reset controls, the predicted class, and the JSON response. Do not open `/predict` directly; that endpoint expects a POST request. The URL/port may change when the service tunnel restarts.

For the rolling-update part, use `wine-classifier:v3` as the new Random Forest image tag, then update the Deployment to `wine-classifier:v3`.
