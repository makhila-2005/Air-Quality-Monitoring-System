import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.utils import resample
from xgboost import XGBClassifier
import joblib

# Load data
df = pd.read_csv("Preprocessed_Indoor_Air_Quality.csv")

# Encode target
le = LabelEncoder()
df['Ventilation Status'] = le.fit_transform(df['Ventilation Status'])  # Open=1, Closed=0

# Features & target
X = df.drop(columns=['Ventilation Status'])
y = df['Ventilation Status']

# Print class distribution
print("\n📊 Target distribution before split:")
print(y.value_counts())

# Stratified Split
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_idx, test_idx in split.split(X, y):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

# Combine for resampling
train_data = pd.concat([X_train, y_train], axis=1)
majority = train_data[train_data['Ventilation Status'] == 0]
minority = train_data[train_data['Ventilation Status'] == 1]

print("\n✅ Training class counts:")
print("Majority (0):", len(majority))
print("Minority (1):", len(minority))

# Safety check
if len(majority) == 0 or len(minority) == 0:
    raise ValueError("One of the classes has 0 samples in the training set. Cannot proceed with resampling.")

# Oversample minority
minority_upsampled = resample(minority, 
                               replace=True,
                               n_samples=len(majority),
                               random_state=42)

# Concatenate balanced data
upsampled = pd.concat([majority, minority_upsampled])
X_train_bal = upsampled.drop(columns=['Ventilation Status'])
y_train_bal = upsampled['Ventilation Status']

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_bal)
X_test_scaled = scaler.transform(X_test)

# Train XGBoost model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_train_scaled, y_train_bal)

# Evaluate
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print("\n🎯 Test Accuracy:", round(accuracy, 4))

# Save model and transformers
joblib.dump(model, "ventilation_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le, "label_encoder.pkl")
print("✅ Model, scaler, and encoder saved.")
