import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
# Load the dataset
df=pd.read_csv("IoT_Indoor_Air_Quality_Dataset.csv",encoding='cp1252')

# Display first few rows
print("First few rows of the dataset:")
print(df.head())

# Convert 'Time' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df = df.drop('Timestamp', axis=1)
df = df.drop('PM2.5 (?g/m?)', axis=1)
df = df.drop('PM10 (?g/m?)', axis=1)
#df = df.drop('Occupancy Count', axis=1)

# Check for null or NaN values
print("\nMissing values per column:")
print(df.isnull().sum())

# Drop rows with any missing values (or handle differently if needed)
df = df.dropna()

# Reset index after dropping rowssss
df = df.reset_index(drop=True)

# Display data types
print("\nData types after cleaning:")
print(df.dtypes)

# Select only numeric columns for scaling
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Scale the numeric features using StandardScaler
scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Show preprocessed data
print("\nPreprocessed and scaled data:")
print(df_scaled.head())

# Save cleaned dataset to CSV
df_scaled.to_csv("Preprocessed_Indoor_Air_Quality.csv", index=False)
print("\n✅ Preprocessed dataset saved as 'Preprocessed_Indoor_Air_Quality.csv'")