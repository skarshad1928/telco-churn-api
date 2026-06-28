# Telecom Customer Churn Prediction System

An end-to-end Machine Learning application that predicts customer churn in the telecommunications industry. The project integrates a trained ML model, REST API, analytics dashboard, and Streamlit-based retention portal to help customer service teams identify high-risk customers and reduce churn.

---

## Project Overview

Customer churn is one of the biggest challenges for telecom companies. This project provides a production-ready solution that predicts whether a customer is likely to leave the service and recommends retention strategies.

The system consists of:

* Machine Learning model for churn prediction
* FastAPI REST API
* Interactive Plotly Dash analytics dashboard
* Streamlit Retention Portal
* Render cloud deployment

---

## Features

* Predict customer churn probability
* Customer risk classification (Low, Medium, High)
* Customer segmentation using K-Means clustering
* REST API for real-time predictions
* Interactive analytics dashboard
* Streamlit portal for Customer Service Representatives
* Automated retention recommendations

---

## Project Architecture

```
                IBM Telco Dataset
                        │
                        ▼
          Data Cleaning & Feature Engineering
                        │
                        ▼
          Machine Learning Model (18 Features)
                        │
                        ▼
               FastAPI REST API (Render)
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
 Analytics Dashboard             Streamlit Portal
 (Business Insights)         (Customer Risk Prediction)
```

---

## Tech Stack

| Category         | Technologies                      |
| ---------------- | --------------------------------- |
| Programming      | Python                            |
| Machine Learning | Scikit-Learn, XGBoost             |
| Data Analysis    | Pandas, NumPy                     |
| Visualization    | Matplotlib, Seaborn, Plotly Dash  |
| Backend          | FastAPI, Uvicorn                  |
| Frontend         | Streamlit                         |
| Deployment       | Render, Streamlit Community Cloud |
| Testing          | Postman                           |
| Dataset          | IBM Telco Customer Churn Dataset  |

---

## Dataset

* **Dataset:** IBM Telco Customer Churn
* **Total Customers:** 7,043
* **Overall Churn Rate:** 26.5%
* **Average Customer Lifetime Value:** $4,400
* **Average Monthly Charges:** $64.76
* **Average Tenure:** 32.4 Months

---

## Machine Learning Pipeline

* Data Cleaning
* Feature Engineering
* Feature Encoding
* Model Training
* Hyperparameter Optimization
* Threshold Optimization
* Customer Segmentation using K-Means
* Model Deployment

The model predicts:

* Churn Probability
* Risk Tier
* Customer Cluster

---

## API

### Health Check

```
GET /
```

Response

```json
{
  "message": "Telco Churn API Running"
}
```

---

### Prediction

```
POST /predict
```

Returns

```json
{
  "assigned_cluster": 1,
  "churn_probability": 0.87,
  "churn_risk_flag": 1,
  "risk_tier": "High Risk"
}
```

---

## Dashboard

The Plotly Dash dashboard provides:

* Customer KPIs
* Churn Rate
* Customer Lifetime Value
* Monthly Charges
* Churn Reasons
* City-wise Analysis
* Customer Segmentation
* Interactive Filtering

---

## Retention Portal

The Streamlit application allows Customer Service Representatives to:

* Enter customer information
* Predict churn risk
* View churn probability
* View customer segment
* Receive retention recommendations

---

## Business Insights

* Competitor offers are the largest driver of churn.
* Month-to-month contracts have the highest churn rate.
* Customers with shorter tenure are more likely to churn.
* Young customers without partners show significantly higher churn.
* Improving customer support quality can reduce churn.

---

## Project Workflow

```
Dataset
   │
   ▼
EDA
   │
   ▼
Feature Engineering
   │
   ▼
Model Training
   │
   ▼
FastAPI Deployment
   │
   ▼
API Testing
   │
   ▼
Analytics Dashboard
   │
   ▼
Streamlit Retention Portal
```

---

## Future Improvements

* Add Redis caching
* Live data pipeline
* Authentication & authorization
* Docker containerization
* Kubernetes deployment
* CI/CD using GitHub Actions
* Monitoring with Prometheus & Grafana
* Automated model retraining
* Cloud database integration

---

## Project Structure

```
├── data/
├── notebooks/
├── model/
├── api/
│   ├── main.py
│   └── requirements.txt
├── dashboard/
├── streamlit_app/
├── images/
├── README.md
└── requirements.txt
```

---

## Limitations

* Render free-tier cold starts
* API timeout during idle periods
* No caching layer
* Static dataset
* Single API dependency
* Limited scalability on free hosting

---

## Results

* 7,043 customer records analyzed
* Real-time churn prediction
* Customer segmentation
* Interactive business dashboard
* End-to-end deployment
* Production-ready REST API

---

## Author

**Your Name**

B.Tech Computer Science Engineering

Machine Learning | Data Science | Full Stack Development

---

## License

This project is developed for educational and portfolio purposes.
