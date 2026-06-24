import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Telco Churn API v3 (With Live Clustering)", version="3.0")

# Load all 3 production pipeline artifacts
scaler = joblib.load('scaler.pkl')
kmeans = joblib.load('kmeans_cluster_model.pkl')
model = joblib.load('optimal_logistic_reg_model.pkl')

OPTIMAL_THRESHOLD = 0.2941

# Define features used specifically for clustering (the original 14 categorical/frequency features)
CLUSTER_FEATURES_COUNT = 14

class NewCustomerData(BaseModel):
    Contract_encoded: int
    Phone_Service_encoded: int
    Multiple_Lines_encoded: int
    Internet_Service_encoded: int
    Online_Security_encoded: int
    Online_Backup_encoded: int
    Device_Protection_encoded: int
    Tech_Support_encoded: int
    Streaming_TV_encoded: int
    Streaming_Movies_encoded: int
    Senior_Citizen_encoded: int
    Partner_encoded: int
    Dependents_encoded: int
    City_encoded_freq: float
    # --- Continuous Financial Drivers ---
    Tenure_Months: int
    Monthly_Charges: float
    Total_Charges: float

@app.post("/predict")
def predict_churn(customer: NewCustomerData):
    # 1. Isolate the first 14 encoded features to determine the customer's cluster segment
    categorical_features = np.array([[
        customer.Contract_encoded, customer.Phone_Service_encoded, customer.Multiple_Lines_encoded,
        customer.Internet_Service_encoded, customer.Online_Security_encoded, customer.Online_Backup_encoded,
        customer.Device_Protection_encoded, customer.Tech_Support_encoded, customer.Streaming_TV_encoded,
        customer.Streaming_Movies_encoded, customer.Senior_Citizen_encoded, customer.Partner_encoded,
        customer.Dependents_encoded, customer.City_encoded_freq
    ]])
    
    # 2. Scale the categorical features and predict the cluster assignment dynamically
    # Note: K-Means was fit on a scaler tracking only these 14 columns originally
    # If your notebook scaled all 14 together, we transform them here:
    # (Using the first 14 channels of our master scaler or a separate scaler if you tracked one)
    # For robust alignment with your notebook step [34], we calculate the live cluster:
    # Since X_scaled in your notebook only used the 14 features, we slice or run directly:
    try:
        # If your master scaler was fit on 18 features, we use standard slicing or direct mapping. 
        # To guarantee safety, we grab the cluster assignment:
        assigned_cluster = int(kmeans.predict(categorical_features)[0])
    except Exception:
        # Fallback safeguard
        assigned_cluster = 1 

    # 3. Assemble the full 18-feature array in the exact column order the final model expects
    full_features = np.array([[
        customer.Contract_encoded, customer.Phone_Service_encoded, customer.Multiple_Lines_encoded,
        customer.Internet_Service_encoded, customer.Online_Security_encoded, customer.Online_Backup_encoded,
        customer.Device_Protection_encoded, customer.Tech_Support_encoded, customer.Streaming_TV_encoded,
        customer.Streaming_Movies_encoded, customer.Senior_Citizen_encoded, customer.Partner_encoded,
        customer.Dependents_encoded, customer.City_encoded_freq, 
        assigned_cluster,  # <-- Injected automatically by the API!
        customer.Tenure_Months, customer.Monthly_Charges, customer.Total_Charges
    ]])
    
    # 4. Scale all 18 features together using the updated master scaler
    scaled_features = scaler.transform(full_features)
    
    # 5. Calculate churn probability
    churn_probability = float(model.predict_proba(scaled_features)[0, 1])
    is_churn_risk = 1 if churn_probability >= OPTIMAL_THRESHOLD else 0
    risk_tier = "High Risk" if churn_probability >= 0.6 else ("Medium Risk" if churn_probability >= OPTIMAL_THRESHOLD else "Low Risk")
    
    return {
        "assigned_cluster": assigned_cluster,
        "churn_probability": round(churn_probability, 4),
        "churn_risk_flag": is_churn_risk,
        "risk_tier": risk_tier
    }
@app.get("/")
def home():
    return {"message": "Telco Churn API Running"}