import pandas as pd
import pickle
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Load dataset
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, "data", "transactions.csv")

df = pd.read_csv(file_path)

# Features and target
X = df.drop("Class", axis=1)
y = df["Class"]

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, os.path.join(base_dir, "models", "scaler.pkl"))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Model Performance:\n")
print(classification_report(y_test, y_pred))

# Save model
with open(os.path.join(base_dir, "models", "model.pkl"), "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model and scaler saved successfully!")