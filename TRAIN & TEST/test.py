import joblib
import numpy as np

# Load the saved model, scaler, and encoder
model = joblib.load("ventilation_model.pkl")
scaler = joblib.load("scaler.pkl")
le = joblib.load("label_encoder.pkl")

# Define the input prompt for each feature
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

print("📥 Enter the following indoor air quality parameters:")

user_input = []
for feature in features:
    while True:
        try:
            value = float(input(f"  ➤ {feature}: "))
            user_input.append(value)
            break
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value.")

# Convert to 2D array and scale
input_array = np.array([user_input])
input_scaled = scaler.transform(input_array)

# Predict ventilation status
prediction = model.predict(input_scaled)[0]

# Decode label back to original form ('Open' or 'Closed')
predicted_label = le.inverse_transform([prediction])[0]

print("\n🔍 Predicted Ventilation Status: ✅", predicted_label)
