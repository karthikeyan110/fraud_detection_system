from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import sys
import os

# ✅ FIX PATH FIRST (IMPORTANT)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports after path fix
from src.predict import predict_transaction
from src.database import create_table, insert_transaction, get_all_transactions

app = FastAPI()

# Create DB table on startup
create_table()


# -------------------------------
# INPUT SCHEMA
# -------------------------------
class Transaction(BaseModel):
    Time: float
    Amount: float

    # V1 to V28
    V1: float; V2: float; V3: float; V4: float; V5: float; V6: float
    V7: float; V8: float; V9: float; V10: float; V11: float; V12: float
    V13: float; V14: float; V15: float; V16: float; V17: float; V18: float
    V19: float; V20: float; V21: float; V22: float; V23: float; V24: float
    V25: float; V26: float; V27: float; V28: float


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def home():
    return {"message": "API working 🚀"}


# -------------------------------
# PREDICTION API
# -------------------------------
@app.post("/predict")
def predict(data: Transaction):
    try:
        input_data = data.dict()

        # ✅ FIX: Ensure correct column order
        columns_order = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

        df = pd.DataFrame([input_data])[columns_order]

        # Model prediction
        score, label, reasons = predict_transaction(df)

        # Save to DB
        insert_transaction(input_data, float(score), label)

        return {
            "fraud_score": float(score),
            "prediction": label,
            "reasons": reasons
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# TRANSACTION HISTORY API
# -------------------------------
@app.get("/transactions")
def get_transactions():
    try:
        data = get_all_transactions()

        # ✅ SAFE MAPPING
        result = []
        for row in data:
            result.append({
                "id": row[0],
                "Time": row[1],
                "Amount": row[2],
                "fraud_score": row[3],
                "label": row[4]
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))