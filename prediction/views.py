from django.shortcuts import render
import joblib
import numpy as np
import requests

# Load models once when server starts
model = joblib.load("ventilation_model.pkl")
scaler = joblib.load("scaler.pkl")
le = joblib.load("label_encoder.pkl")

# Define expected input features
features = [
    'Temperature (?C)',
    'Humidity (%)',
    'CO2 (ppm)',
    'TVOC (ppb)',
    'CO (ppm)',
    'Light Intensity (lux)',
    'Motion Detected (0 or 1)',
    'Occupancy Count'
]

def get_thingspeak_data():
    try:
        channel_id = '3017296'
        url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?results=1'
        data = requests.get(url).json()
        feed = data['feeds'][0]
        return {
            'Temperature': feed.get('field1', 'N/A'),
            'Humidity': feed.get('field2', 'N/A'),
            'CO2': feed.get('field3', 'N/A'),
            'TVOC': feed.get('field4', 'N/A'),
            'CO': feed.get('field5', 'N/A'),
            'Light': feed.get('field6', 'N/A'),
            'Motion': feed.get('field7', 'N/A'),
            'Occupancy': feed.get('field8', 'N/A'),
        }
    except Exception as e:
        return {'Error': f'Could not fetch data: {e}'}

def predict_view(request):
    result = None
    thingspeak_data = get_thingspeak_data()

    if request.method == "POST":
        try:
            # Collect input values from the form in the same order as 'features'
            values = [float(request.POST.get(f)) for f in features]
            input_array = np.array([values])
            scaled = scaler.transform(input_array)
            pred_encoded = model.predict(scaled)[0]
            pred_label = le.inverse_transform([pred_encoded])[0]
            result = 'Bad' if pred_label == 'Open' else 'Good'
        except Exception as e:
            result = f"Error: {e}"

    return render(request, "predict.html", {
        "features": features,
        "result": result,
        "thingspeak": thingspeak_data
    })
