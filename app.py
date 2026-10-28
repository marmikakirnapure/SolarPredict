from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

with open("solar_models.pkl", "rb") as file:
    saved = pickle.load(file)

models = saved["models"]
metrics = saved["metrics"]
features = saved["features"]
best_model = saved["best_model"]
places = [
    "Nagpur",
    "Pune",
    "Mumbai",
    "Jaipur",
    "Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Ahmedabad",
    "Kolkata"
]

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    show_results = False
    predictions = {}
    savings = {}
    form = {}
    place = ""
    tariff = 0

    if request.method == "POST":
        form = request.form.to_dict()
        try:
            place = form["location"]
            if place not in places:
                raise ValueError("Please choose correct city.")

            values = {
                "panel_capacity_kw": float(form["panel_capacity_kw"]),
                "sunlight_hours": float(form["sunlight_hours"]),
                "solar_irradiance_kwh_m2_day": float(form["solar_irradiance_kwh_m2_day"]),
                "temperature_c": float(form["temperature_c"]),
                "cloud_cover_pct": float(form["cloud_cover_pct"]),
                "humidity_pct": float(form["humidity_pct"]),
                "panel_tilt_deg": float(form["panel_tilt_deg"]),
                "panel_efficiency_pct": float(form["panel_efficiency_pct"]),
                "system_loss_pct": float(form["system_loss_pct"]),
                "month": int(form["month"])
            }
            tariff = float(form["tariff"])

            if values["panel_capacity_kw"] <= 0:
                raise ValueError("Panel capacity must be greater than zero.")
            if not 0 <= values["sunlight_hours"] <= 24:
                raise ValueError("Sunlight hours must be between 0 and 24.")
            if not 1 <= values["month"] <= 12:
                raise ValueError("Please choose a month.")
            if values["solar_irradiance_kwh_m2_day"] < 0:
                raise ValueError("Solar irradiance cannot be negative.")
            for field in ["cloud_cover_pct", "humidity_pct",
                          "panel_efficiency_pct", "system_loss_pct"]:
                if not 0 <= values[field] <= 100:
                    raise ValueError(field.replace("_", " ").title() + " must be between 0 and 100.")
            if not 0 <= values["panel_tilt_deg"] <= 90:
                raise ValueError("Panel tilt must be between 0 and 90 degrees.")
            if tariff < 0:
                raise ValueError("Electricity tariff cannot be negative.")

            row = pd.DataFrame([values], columns=features)
            for name, model in models.items():
                energy = max(0, float(model.predict(row)[0]))
                predictions[name] = energy
                savings[name] = energy * tariff
            show_results = True
        except (ValueError, KeyError) as problem:
            error = str(problem) or "Please check your inputs."
        except Exception:
            error = "Could not make a prediction. Please check your inputs."

    return render_template(
        "index.html", error=error, show_results=show_results,
        predictions=predictions, savings=savings, metrics=metrics,
        best_model=best_model, best_prediction=predictions.get(best_model),
        best_savings=savings.get(best_model), places=places, months=months,
        form=form, place=place
    )

if __name__ == "__main__":
    app.run()
