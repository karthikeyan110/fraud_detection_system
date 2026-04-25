import pandas as pd
from predict import predict_transaction

# Load real dataset
df = pd.read_csv("data/transactions.csv")

# Take a real row (fraud example)
fraud_row = df[df["Class"] == 1].iloc[0]

# Remove label
fraud_input = fraud_row.drop("Class")

# Convert to DataFrame
fraud_input = pd.DataFrame([fraud_input])

prob, label = predict_transaction(fraud_input)

print(f"Fraud Probability: {prob:.4f}")
print(f"Prediction: {label}")