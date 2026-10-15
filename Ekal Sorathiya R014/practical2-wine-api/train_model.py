from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

wine = load_wine()
X, y = wine.data, wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# model = DecisionTreeClassifier(max_depth=4, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
joblib.dump(model, "wine_model.joblib")

print(f"Test accuracy: {accuracy:.3f}")
print("Saved model: wine_model.joblib")
print(f"Feature count: {X.shape[1]}")
print(f"Target classes: {list(wine.target_names)}")
