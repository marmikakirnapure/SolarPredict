import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Read and prepare the real project dataset.
data = pd.read_excel("solar_energy_savings_dataset.xlsx")
data.columns = data.columns.str.strip()
data["date"] = pd.to_datetime(data["date"], errors="coerce")
data["month"] = data["date"].dt.month

features = [
    "panel_capacity_kw", "sunlight_hours",
    "solar_irradiance_kwh_m2_day", "temperature_c",
    "cloud_cover_pct", "humidity_pct", "panel_tilt_deg",
    "panel_efficiency_pct", "system_loss_pct", "month"
]

for column in features + ["energy_generated_kwh"]:
    data[column] = pd.to_numeric(data[column], errors="coerce")
data = data.replace([np.inf, -np.inf], np.nan)
data = data.dropna(subset=["energy_generated_kwh"])

X = data[features]
y = data["energy_generated_kwh"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

algorithms = {
    "Linear Regression": LinearRegression(),
    "KNN Regressor": KNeighborsRegressor(n_neighbors=5),
    "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
    "Random Forest Regressor": RandomForestRegressor(
        n_estimators=100, random_state=42
    )
}

models = {}
metrics = {}
for name, algorithm in algorithms.items():
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        algorithm
    )
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    models[name] = model
    metrics[name] = {
        "MAE": float(mean_absolute_error(y_test, prediction)),
        "RMSE": float(np.sqrt(mean_squared_error(y_test, prediction))),
        "R2": float(r2_score(y_test, prediction))
    }

best_model = min(metrics, key=lambda name: metrics[name]["RMSE"])
with open("solar_models.pkl", "wb") as file:
    pickle.dump({"models": models, "metrics": metrics,
                 "features": features, "best_model": best_model}, file)

print("Model trained successfully.")
