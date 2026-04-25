# 🚨 AI-Powered Real-Time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)

An end-to-end, real-time machine learning dashboard built to detect fraudulent financial transactions instantly. This system features an auto-generating transaction simulator, a highly accurate Random Forest model, and a live-updating interactive dashboard.

## ✨ Key Features

- **🧠 Advanced Machine Learning Model:** Powered by a `RandomForestClassifier` (200 estimators) trained with `class_weight="balanced"` to expertly handle heavily imbalanced fraud datasets.
- **🔄 Real-Time Auto-Simulation:** The dashboard automatically generates, predicts, and logs new transactions into the database natively every 2 seconds, simulating a live financial stream.
- **🚨 Instant Fraud Alerts:** Utilizes dynamic popups (`st.toast` and `st.error`) to alert the user the millisecond a fraudulent transaction enters the system.
- **📊 Interactive Visualizations:** Features real-time pie charts, smoothed trend charts, and a dynamic bar chart breaking down the exact mathematical reasons *why* a transaction was flagged as fraud.
- **💾 Local Database:** All simulated transactions and their predictions are safely stored and queried using an integrated SQLite database.

## 🛠️ Technology Stack

- **Frontend:** Streamlit (Python)
- **Machine Learning:** Scikit-Learn, Pandas
- **Data Scaling:** StandardScaler (joblib)
- **Database:** SQLite3
- **Visualization:** Matplotlib

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/karthikeyan110/fraud_detection_system.git
   cd fraud_detection_system
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard:**
   ```bash
   streamlit run app/app.py
   ```
   *(The dashboard will launch automatically at `http://localhost:8501`)*

## 📂 Project Structure
```text
fraud_detection_system/
├── app/                  # Frontend Streamlit Application
│   └── app.py            # Main dashboard, UI, and auto-simulation loop
├── src/                  # Core Logic & Machine Learning
│   ├── predict.py        # Inference logic and model loading
│   ├── train.py          # Script for training the Random Forest model
│   └── database.py       # SQLite database connection and insert logic
├── models/               # Saved ML Assets
│   ├── model.pkl         # Trained Random Forest model
│   └── scaler.pkl        # StandardScaler for feature normalization
├── requirements.txt      # Python dependencies
└── transactions.db       # Live SQLite database tracking transactions
```

---
*Created as a demonstration of applying Machine Learning to real-world, high-stakes streaming data.*
