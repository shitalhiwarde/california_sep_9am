from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
import joblib

print("Loading California Housing dataset...")

data = fetch_california_housing()

model = RandomForestRegressor(
    n_estimators=20,
    random_state=42,
    n_jobs=-1
)

print("Training model...")

model.fit(data.data, data.target)

joblib.dump(model, "california.joblib")

print("Model saved successfully!")