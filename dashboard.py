import streamlit as st
import requests

# Page layout configuration
st.set_page_config(
    page_title="Telco Customer Retention Portal",
    page_icon="🎯",
    layout="wide"
)

st.title("Telecom Retention Portal & Risk Assessor (v3.0)")
st.markdown("""
This interface evaluates a customer's profile using the newly optimized 18-feature engine. 
The backend API dynamically computes **Unsupervised Cluster Segments** and applies our **Optimal Risk Threshold (0.2941)** to yield precise retention directives.
""")

st.markdown("---")

# Organize inputs into logical dashboard columns
col_demo, col_serv, col_fin = st.columns(3)

with col_demo:
    st.subheader("👤 Customer Demographics")
    senior = st.selectbox("Is Senior Citizen?", ["No", "Yes"])
    partner = st.selectbox("Has Partner?", ["No", "Yes"])
    dependents = st.selectbox("Has Dependents?", ["No", "Yes"])
    
    st.markdown("##### Geographic Footprint")
    # Defaulting to the mean/median frequency scales found in your EDA
    city_size = st.slider("City Market Frequency Share", 0.0005, 0.05, 0.0433, step=0.0005, format="%.4f")

with col_serv:
    st.subheader("📦 Core Services & Contracts")
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet Service Type", ["No", "DSL", "Fiber optic"])
    phone = st.selectbox("Phone Line Active?", ["No", "Yes"])
    lines = st.selectbox("Multiple Lines Service", ["No phone service", "No", "Yes"])
    
    st.markdown("##### Security & Entertainment Add-ons")
    security = st.selectbox("Online Security Add-on", ["No internet service", "No", "Yes"])
    backup = st.selectbox("Online Backup Add-on", ["No internet service", "No", "Yes"])
    device = st.selectbox("Device Protection Plan", ["No internet service", "No", "Yes"])
    support = st.selectbox("Premium Tech Support", ["No internet service", "No", "Yes"])
    tv = st.selectbox("Streaming TV Plans", ["No internet service", "No", "Yes"])
    movies = st.selectbox("Streaming Movies Plans", ["No internet service", "No", "Yes"])

with col_fin:
    st.subheader("💳 Financial & Tenure Drivers")
    tenure = st.slider("Tenure Length (Months)", min_value=0, max_value=72, value=12)
    monthly_charges = st.number_input("Monthly Bill Charges ($)", min_value=18.0, max_value=120.0, value=65.0, step=0.5)
    
    # Intelligently pre-calculate total charges based on selections to save users time
    calculated_est_total = round(float(tenure * monthly_charges), 2)
    total_charges = st.number_input("Total Lifetime Charges ($)", min_value=0.0, value=calculated_est_total, step=10.0)

# --- MAP STRINGS DIRECTLY TO YOUR EXACT NOTEBOOK ENCODING RULES ---
mapping_binary = {"No": 1, "Yes": 0}  # Matches Senior, Partner, Dependents custom mappings
mapping_standard = {"No phone service": 0, "No internet service": 0, "No": 2, "Yes": 1}
contract_map = {"Two year": 0, "One year": 1, "Month-to-month": 2}
internet_map = {"No": 0, "DSL": 1, "Fiber optic": 2}

# Package payload matching your Pydantic Schema exactly
payload = {
    "Contract_encoded": contract_map[contract],
    "Phone_Service_encoded": 1 if phone == "Yes" else 0,
    "Multiple_Lines_encoded": mapping_standard[lines],
    "Internet_Service_encoded": internet_map[internet],
    "Online_Security_encoded": mapping_standard[security],
    "Online_Backup_encoded": mapping_standard[backup],
    "Device_Protection_encoded": mapping_standard[device],
    "Tech_Support_encoded": mapping_standard[support],
    "Streaming_TV_encoded": mapping_standard[tv],
    "Streaming_Movies_encoded": mapping_standard[movies],
    "Senior_Citizen_encoded": mapping_binary[senior],
    "Partner_encoded": mapping_binary[partner],
    "Dependents_encoded": mapping_binary[dependents],
    "City_encoded_freq": city_size,
    # New financial inputs passed straight over
    "Tenure_Months": tenure,
    "Monthly_Charges": monthly_charges,
    "Total_Charges": total_charges
}

st.markdown("---")

# Execution and Evaluation Trigger
if st.button("🚀 Run Risk Analysis Profile", use_container_width=True):
    try:
        # Route request payload directly to your running FastAPI backend port
        response = requests.post("https://telco-churn-api-gbyx.onrender.com/predict", json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Parse return variables
        prob = result["churn_probability"]
        tier = result["risk_tier"]
        flag = result["churn_risk_flag"]
        cluster_assignment = result["assigned_cluster"]
        
        # Display Key Score Metrics cards
        out_col1, out_col2, out_col3 = st.columns(3)
        with out_col1:
            st.metric(label="Calculated Churn Probability", value=f"{prob * 100:.2f}%")
        with out_col2:
            st.metric(label="System Risk Classification", value=tier)
        with out_col3:
            st.metric(label="Auto-Assigned Customer Cluster", value=f"Cluster {cluster_assignment}")
            
        st.markdown("### 🛠️ Tailored Operational Action Plan")
        
        if flag == 1:
            st.error("🚨 CRITICAL ATTRITION RISK SIGNAL TRIGGERED")
            
            # Smart Diagnostic Breakdown based on values input
            st.markdown("#### **Risk Factor Attribution:**")
            factors = []
            if contract == "Month-to-month":
                factors.append("• **Contract Structure Vulnerability:** Customers on short-term rolling month-to-month bills have zero exit friction.")
            if tenure < 6:
                factors.append("• **Early Lifecycle Defection:** Customer is within their critical initial onboarding runway (under 6 months tenure).")
            if internet == "Fiber optic" and security == "No":
                factors.append("• **Unprotected High-Value Account:** Fiber optic accounts represent high-velocity churn vectors when missing supplementary security features like Online Security.")
            if monthly_charges > 85.0 and contract == "Month-to-month":
                factors.append("• **High Monthly Price Sensitivity:** Premium spend combined with a short-term contract creates immediate competitor-sniping risks.")
                
            st.write("\n".join(factors) if factors else "• Risk is driven by systemic interaction across multiple behavioral service metrics.")
            
            # Actionable Playbook Strategy Recommendations
            st.markdown("#### **Prescriptive Retention Interventions:**")
            if contract == "Month-to-month":
                st.info("💡 **Contract Migration Play:** Propose an immediate migration to a **1-Year commitment plan** with an introductory $10/month loyalty credit.")
            if security == "No" or support == "No":
                st.info("💡 **Feature Enrichment Bundle:** Add **Premium Tech Support & Online Security** for 6 months free of charge to increase platform stickiness.")
            if tenure < 6:
                st.warning("📞 **Proactive Outreach:** Route this account to the Customer Success Onboarding squad within 24 hours for a health-check call.")
        else:
            st.success("✅ STABLE ACCOUNT STANDING")
            st.markdown("#### **Growth & Expansion Playbook:**")
            st.write("• This customer profile scores safely below our intervention threshold. Focus on positive relationship tracking.")
            if security == "No" or backup == "No":
                st.info("📢 **Upsell Play:** Target this customer during standard renewal tracks for digital protection expansion add-ons.")

    except requests.exceptions.ConnectionError:
        st.error("🔴 **API Connection Error:** Could not contact the FastAPI backend server on `http://127.0.0.1:8000`. Ensure your API server is booted and running in your terminal window!")