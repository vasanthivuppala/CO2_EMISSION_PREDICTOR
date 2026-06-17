import streamlit as st
import pickle
import pandas as pd
model = pickle.load(open("co2_model.pkl", "rb"))
preprocessor = pickle.load(open("preprocessor.pkl", "rb"))
st.set_page_config(
    page_title="CO₂ Emission Predictor",
    page_icon="🚗",
    layout="centered"
)
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1 {
    text-align: center;
}

.stButton > button {
   height: 60px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 15px;
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white;
}

.stDownloadButton > button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>🚗 CO₂ EMISSION PREDICTOR</h1>
<h4 style='text-align:center;color:gray'>
AI Powered Vehicle Emission Analytics
</h4>
""", unsafe_allow_html=True)

st.divider()

left, right = st.columns([1.2,1.3])
with right:
    st.markdown("""
    <div style="
        padding:40px;
        border-radius:20px;
        border:2px solid #7c3aed;
box-shadow: 0 0 20px rgba(124,58,237,0.4);
        text-align:center;
        margin-top:70px;
    ">
        <h2>🚗 CO₂ Prediction Result</h2>
        <p>Fill vehicle details and click Predict</p>
    </div>
    """, unsafe_allow_html=True)

with left:

    st.subheader("🚗 Vehicle Information")

    col1, col2 = st.columns(2)

    with col1:
        make = st.selectbox(
            "Vehicle Make",
            [
                "ACURA",
                "AUDI",
                "BMW",
                "CHEVROLET",
                "FORD",
                "HONDA",
                "TOYOTA"
            ]
        )

        transmission = st.selectbox(
            "Transmission",
            [
                "A4",
                "A5",
                "A6",
                "A8",
                "M5",
                "M6",
                "AS6",
                "AS8"
            ]
        )

        model_year = st.number_input(
            "Model Year",
            min_value=1995,
            max_value=2025,
            value=2020
        )

        cylinders = st.number_input(
            "Number of Cylinders",
            min_value=2,
            max_value=16,
            value=4
        )

    with col2:
        vehicle_class = st.selectbox(
            "Vehicle Class",
            [
                "COMPACT",
                "MID - SIZE",
                "SUV",
                "SUBCOMPACT",
                "FULL - SIZE",
                "MINIVAN"
            ]
        )

        fuel_type = st.selectbox(
            "Fuel Type",
            ["X", "Z", "D", "E", "N"]
        )

        engine_size = st.number_input(
            "Engine Size (L)",
            min_value=0.5,
            max_value=10.0,
            value=2.0
        )

        fuel_consumption = st.number_input(
            "Fuel Consumption Combined (L/100 km)",
            min_value=1.0,
            max_value=30.0,
            value=8.0
        )

    st.divider()

    predict_btn = st.button(
    "🚗 Predict CO₂ Emission",
    use_container_width=True
)

if predict_btn:

    input_data = pd.DataFrame({
        'MODEL YEAR': [model_year],
        'MAKE': [make],
        'VEHICLE CLASS': [vehicle_class],
        'ENGINE SIZE (L)': [engine_size],
        'CYLINDERS': [cylinders],
        'TRANSMISSION': [transmission],
        'FUEL TYPE': [fuel_type],
        'FUEL CONSUMPTION COMB (L/100 km)': [fuel_consumption]
    })

    processed_data = preprocessor.transform(input_data)

    prediction = model.predict(processed_data)

    report_df = pd.DataFrame({
        "Attribute": [
            "Model Year",
            "Make",
            "Vehicle Class",
            "Engine Size (L)",
            "Cylinders",
            "Transmission",
            "Fuel Type",
            "Fuel Consumption (L/100 km)",
            "Predicted CO2 Emission (g/km)"
        ],
        "Value": [
            model_year,
            make,
            vehicle_class,
            engine_size,
            cylinders,
            transmission,
            fuel_type,
            fuel_consumption,
            round(prediction[0], 2)
        ]
    })

    csv = report_df.to_csv(index=False)

    co2 = prediction[0]

    if co2 < 180:
        category = "🟢 Low Emission"
        border_color = "#22c55e"

    elif co2 < 300:
        category = "🟡 Moderate Emission"
        border_color = "#f59e0b"

    else:
        category = "🔴 High Emission"
        border_color = "#ef4444"

    with right:

        st.markdown(
            f"""
            <div style="
                padding:25px;
                border-radius:15px;
                border:3px solid {border_color};
                text-align:center;
                margin-top:20px;
                margin-bottom:20px;
            ">
                <h3>🚗 Predicted CO₂ Emission</h3>
                <h1>{co2:.2f} g/km</h1>
                <h4>{category}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            label="📥 Download Vehicle Report",
            data=csv,
            file_name="vehicle_emission_report.csv",
            mime="text/csv",
            use_container_width=True
        )