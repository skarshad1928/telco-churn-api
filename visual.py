import os
os.environ["FLASK_SKIP_DOTENV"] = "1"

import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# --------------------
# Load Data
# --------------------
df = pd.read_excel("Telco_customer_churn.xlsx")
df.columns = df.columns.str.strip()

# --------------------
# App
# --------------------
app = dash.Dash(__name__)
server = app.server

# --------------------
# Layout
# --------------------
app.layout = html.Div(

    [

        html.H1(
            "Customer Churn Analysis Dashboard",
            style={
                "textAlign": "center",
                "color": "#0A66C2"
            }
        ),

        html.P(
            "Interactive Dashboard for Customer Retention Insights",
            style={
                "textAlign": "center",
                "color": "gray"
            }
        ),

        # Filters
        html.Div([

            dcc.Dropdown(
                id="city-dropdown",
                options=[
                    {"label": city, "value": city}
                    for city in sorted(df["City"].dropna().unique())
                ],
                placeholder="Select City"
            ),

            dcc.Dropdown(
                id="senior-dropdown",
                options=[
                    {"label": x, "value": x}
                    for x in sorted(df["Senior Citizen"].dropna().unique())
                ],
                placeholder="Senior Citizen"
            ),

            dcc.Dropdown(
                id="partner-dropdown",
                options=[
                    {"label": x, "value": x}
                    for x in sorted(df["Partner"].dropna().unique())
                ],
                placeholder="Partner"
            )

        ],

        style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr 1fr",
            "gap": "15px",
            "marginBottom": "25px"
        }),

        # KPI Cards
        html.Div(
            id="kpi-container",
            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "20px",
                "flexWrap": "wrap"
            }
        ),

        html.Br(),

        # Graphs
        html.Div([

            dcc.Graph(id="churn-reason-chart"),

            dcc.Graph(id="cltv-score-chart")

        ])

    ],

    style={
        "padding": "30px",
        "backgroundColor": "#F4F6F9",
        "minHeight": "100vh"
    }

)

# --------------------
# Callback
# --------------------
@app.callback(
    Output("kpi-container", "children"),
    Output("churn-reason-chart", "figure"),
    Output("cltv-score-chart", "figure"),

    Input("city-dropdown", "value"),
    Input("senior-dropdown", "value"),
    Input("partner-dropdown", "value")
)
def update_dashboard(city, senior, partner):

    filtered_df = df.copy()

    if city:
        filtered_df = filtered_df[
            filtered_df["City"] == city
        ]

    if senior:
        filtered_df = filtered_df[
            filtered_df["Senior Citizen"] == senior
        ]

    if partner:
        filtered_df = filtered_df[
            filtered_df["Partner"] == partner
        ]

    # KPIs
    total_customers = len(filtered_df)

    churn_pct = (
        (filtered_df["Churn Label"] == "Yes").mean() * 100
        if "Churn Label" in filtered_df.columns
        else 0
    )

    avg_cltv = filtered_df["CLTV"].mean()

    avg_tenure = filtered_df["Tenure Months"].mean()

    avg_monthly_charges = filtered_df["Monthly Charges"].mean()

    kpis = [
        ("Total Customers", f"{total_customers:,}"),
        ("Customer Churn %", f"{churn_pct:.1f}%"),
        ("Average CLTV", f"${avg_cltv:,.0f}"),
        ("Average Tenure", f"{avg_tenure:.1f} Months"),
        ("Avg Monthly Charges", f"${avg_monthly_charges:.2f}")
    ]

    cards = []

    for title, value in kpis:

        cards.append(

            html.Div(

                [
                    html.H4(title),

                    html.H2(
                        value,
                        style={"color": "#0A66C2"}
                    )
                ],

                style={
                    "backgroundColor": "white",
                    "padding": "20px",
                    "width": "220px",
                    "borderRadius": "12px",
                    "boxShadow": "0px 3px 10px rgba(0,0,0,0.1)",
                    "textAlign": "center"
                }

            )

        )

    # --------------------
    # Top 5 Churn Reasons
    # --------------------

    churn_reason_fig = px.bar(
        title="Top 5 Churn Reasons"
    )

    if "Churn Reason" in filtered_df.columns:

        churn_reason_df = filtered_df[
            filtered_df["Churn Reason"].notna()
        ]

        if len(churn_reason_df) > 0:

            top_reasons = (
                churn_reason_df["Churn Reason"]
                .value_counts()
                .head(5)
                .reset_index()
            )

            top_reasons.columns = [
                "Reason",
                "Count"
            ]

            churn_reason_fig = px.bar(
                top_reasons,
                x="Reason",
                y="Count",
                text="Count",
                title="Top 5 Churn Reasons"
            )

    # --------------------
    # CLTV vs Churn Score
    # --------------------

    cltv_fig = px.scatter(
        filtered_df,
        x="Churn Score",
        y="CLTV",
        color="Churn Label",
        trendline="ols",
        hover_data=["City"],
        title="CLTV vs Churn Score"
    )

    cltv_fig.update_layout(
        xaxis_title="Churn Score",
        yaxis_title="Customer Lifetime Value (CLTV)"
    )

    return (
        cards,
        churn_reason_fig,
        cltv_fig
    )

# --------------------
# Run
# --------------------
if __name__ == "__main__":
    app.run(debug=False)