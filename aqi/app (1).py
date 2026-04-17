import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model/aqi_model.pkl", "rb"))

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/clean_aqi.csv")
df['Date'] = pd.to_datetime(df['Date'])

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AQI Dashboard", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0f172a, #1e293b);}
.card {
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
}
.green {background:#2e7d32;}
.yellow {background:#f9a825;}
.orange {background:#ef6c00;}
.red {background:#c62828;}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🌍 AQI Predictor & Health Advisor")

# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("🔬 Enter Pollutant Values")

pm25 = st.sidebar.slider("PM2.5", 0, 500, 50)
pm10 = st.sidebar.slider("PM10", 0, 500, 80)
no2 = st.sidebar.slider("NO2", 0, 200, 30)
co = st.sidebar.slider("CO", 0.0, 10.0, 1.0)

# ---------------- CITY SELECT ----------------
st.subheader("📍 Select City")
city = st.selectbox("City", df['City'].unique())

# ---------------- PREDICT BUTTON ----------------
if st.button("🔮 Predict AQI"):

    input_data = np.array([[pm25, pm10, no2, co]])
    aqi = int(model.predict(input_data)[0])

    # ---------------- CLASSIFICATION ----------------
    def classify(aqi):
        if aqi <= 50:
            return "Good", "green"
        elif aqi <= 100:
            return "Moderate", "yellow"
        elif aqi <= 200:
            return "Poor", "orange"
        else:
            return "Hazardous", "red"

    category, color = classify(aqi)

    # ---------------- CARDS ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="card green">Current AQI<br><h1>{aqi}</h1></div>', unsafe_allow_html=True)

    with col2:
        tomorrow = int(aqi * 1.05)
        st.markdown(f'<div class="card red">Predicted AQI<br><h1>{tomorrow}</h1></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="card {color}">Status<br><h2>{category}</h2></div>', unsafe_allow_html=True)

    # ---------------- HEALTH ADVISORY ----------------
    st.subheader("🏥 Health Advisory")

    if category == "Good":
        st.success("🟢 Air Quality is Good")
        st.write("• Safe for outdoor activities")
        st.write("• No health risk")
        st.write("• Enjoy exercise and fresh air")

    elif category == "Moderate":
        st.warning("🟡 Moderate Air Quality")
        st.write("• Sensitive groups should reduce prolonged outdoor exertion")
        st.write("• Mild irritation possible for some people")
        st.write("• Keep windows ventilated")

    elif category == "Poor":
        st.error("🟠 Poor Air Quality")
        st.write("• Avoid outdoor activities")
        st.write("• Wear masks if going outside")
        st.write("• People with asthma should be cautious")
        st.write("• Keep indoor air clean")

    elif category == "Hazardous":
        st.error("🔴 Hazardous Air Quality")
        st.write("• Stay indoors as much as possible")
        st.write("• Use air purifiers if available")
        st.write("• Avoid physical activity")
        st.write("• Serious health risk for everyone")

    # Extra alert
    if aqi > 200:
        st.warning("⚠️ ALERT: Very unhealthy air! Limit all outdoor exposure.")

# ---------------- HISTORICAL TREND ----------------
st.subheader("📈 Historical AQI Trend")

city_data = df[df['City'] == city]
trend = city_data.groupby('Date')['AQI'].mean()

st.line_chart(trend)

# ---------------- CITY COMPARISON ----------------
st.subheader("🏙️ City-wise AQI Comparison")

city_avg = df.groupby('City')['AQI'].mean().sort_values(ascending=False)
st.bar_chart(city_avg.head(10))

# ---------------- POLLUTANT DISPLAY ----------------
st.subheader("🔬 Pollutant Levels")

st.write(f"PM2.5: {pm25}")
st.write(f"PM10: {pm10}")
st.write(f"NO2: {no2}")
st.write(f"CO: {co}")