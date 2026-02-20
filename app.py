import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Mental Wellness Dashboard", layout="wide")

st.title("🧠 AI-Powered Mental Wellness Monitoring System")

# --------------------------------------------------
# GOOGLE SHEET CONNECTION
# --------------------------------------------------

sheet_id = "1pgq7hu_6mUzNUXVeObk4_3HnY0fTE7tnJd7QoCzZemc"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

df = pd.read_csv(url)

# Clean column names
df.columns = df.columns.str.strip()

# Convert Timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# --------------------------------------------------
# SIDEBAR FILTER
# --------------------------------------------------

st.sidebar.header("📊 Data Filter")

filter_option = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"]
)

if filter_option == "Last 7 Days":
    df = df[df["Timestamp"] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
elif filter_option == "Last 30 Days":
    df = df[df["Timestamp"] >= pd.Timestamp.now() - pd.Timedelta(days=30)]

# --------------------------------------------------
# STRESS COLUMN SETUP
# --------------------------------------------------

stress_column = "How stressed do you feel today?"
mood_column = "How are you feeling today?"

df[stress_column] = pd.to_numeric(df[stress_column], errors="coerce")

# --------------------------------------------------
# METRICS SECTION
# --------------------------------------------------

total_entries = len(df)
avg_stress = df[stress_column].mean()
high_risk_count = len(df[df[stress_column] >= 4])

col1, col2, col3 = st.columns(3)

col1.metric("Total Entries", total_entries)
col2.metric("Average Stress Level", round(avg_stress, 2))
col3.metric("High Risk Cases", high_risk_count)

st.divider()

# --------------------------------------------------
# CREATE DISPLAY STRESS COLUMN
# --------------------------------------------------

stress_map = {
    1: "Very Low",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Very High"
}

df["Stress Level"] = df[stress_column].map(stress_map)

# --------------------------------------------------
# HIGH RISK ALERT SECTION
# --------------------------------------------------

st.subheader("🚨 High Risk Alerts")

high_risk_df = df[df[stress_column] >= 4]

if len(high_risk_df) > 0:
    st.error(f"{len(high_risk_df)} high-risk entries detected")
    st.dataframe(
        high_risk_df[["Your Name", "Your Email Address", "Stress Level"]],
        use_container_width=True
    )
else:
    st.success("No high-risk cases detected")

st.divider()

# --------------------------------------------------
# STRESS TREND LINE GRAPH
# --------------------------------------------------

st.subheader("📈 Stress Trend Over Time")

trend_df = df.sort_values("Timestamp")
trend_df = trend_df.set_index("Timestamp")

st.line_chart(trend_df[stress_column])

st.divider()

# --------------------------------------------------
# MOOD DISTRIBUTION PIE CHART
# --------------------------------------------------

st.subheader("🥧 Mood Distribution")

mood_counts = df[mood_column].value_counts()

fig, ax = plt.subplots()
ax.pie(mood_counts, labels=mood_counts.index, autopct="%1.1f%%")
ax.set_title("Mood Distribution")

st.pyplot(fig)

st.divider()

# --------------------------------------------------
# STRESS DISTRIBUTION BAR CHART
# --------------------------------------------------

st.subheader("📊 Stress Level Distribution")

stress_counts = df["Stress Level"].value_counts()
st.bar_chart(stress_counts)

st.divider()

# --------------------------------------------------
# AI GENERATED SUMMARY SECTION
# --------------------------------------------------

st.subheader("🤖 AI Summary & Insights")

if total_entries > 0:

    summary = f"""
    • The average stress level during the selected period is **{round(avg_stress,2)}**.
    
    • There are **{high_risk_count} high-risk cases** detected.
    
    • The most common mood reported is **{mood_counts.idxmax()}**.
    """

    if avg_stress >= 4:
        summary += "\n⚠️ Overall stress levels are significantly high. Preventive intervention is recommended."
    elif avg_stress >= 3:
        summary += "\n⚡ Stress levels are moderate. Monitoring is advised."
    else:
        summary += "\n✅ Overall stress levels appear stable."

    st.info(summary)

else:
    st.warning("No data available for selected period.")

st.divider()

# --------------------------------------------------
# SHOW FULL TABLE
# --------------------------------------------------

st.subheader("📄 Recent Entries")

df_display = df.drop(columns=[stress_column])
st.dataframe(df_display, use_container_width=True)
