import joblib
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, "models", "model.pkl")
scaler_path = os.path.join(base_dir, "models", "scaler.pkl")

# Use joblib to load both since we'll have a joblib scaler
import pickle
try:
    model = joblib.load(model_path)
except Exception:
    # fallback to pickle if it wasn't saved with joblib yet
    with open(model_path, "rb") as f:
        model = pickle.load(f)

scaler = joblib.load(scaler_path)

def predict_transaction(df):
    df_scaled = scaler.transform(df)

    score = model.predict_proba(df_scaled)[0][1]
    label = "FRAUD" if score > 0.5 else "NORMAL"

    reasons = []
    if df["Amount"].values[0] > 50000:
        reasons.append("Very large transaction")
    if df["Time"].values[0] < 10000:
        reasons.append("Odd transaction time")

    return score, label, reasons