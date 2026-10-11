from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("california.joblib")

FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        values = [float(data[name]) for name in FEATURES]
        input_df = pd.DataFrame([values], columns=FEATURES)

        prediction = float(model.predict(input_df)[0])

        # Standard California Housing target is measured
        # in units of $100,000.
        price = prediction * 100000

        return jsonify({
            "success": True,
            "prediction": round(price, 2),
            "formatted_price": f"${price:,.2f}"
        })

    except (KeyError, TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": f"Invalid input: {error}"
        }), 400

    except Exception:
        app.logger.exception("Prediction error")
        return jsonify({
            "success": False,
            "error": "Prediction failed. Check your model and its input features."
        }), 500

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)