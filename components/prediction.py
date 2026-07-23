import streamlit as st
import pickle
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from utils import clean_feature_name
from database import save_prediction


# Load model and preprocessor
model = pickle.load(open("co2_model.pkl", "rb"))
preprocessor = pickle.load(open("preprocessor.pkl", "rb"))

# Load dataset for dropdown values
dataset = pd.read_csv("MY1995_2023.csv", encoding="latin1")

background = pd.read_csv("training_data.csv")
background_processed = preprocessor.transform(background)

explainer = shap.TreeExplainer(model)

# Dropdown options
makes = sorted(dataset["MAKE"].dropna().unique())
vehicle_classes = sorted(dataset["VEHICLE CLASS"].dropna().unique())
transmissions = sorted(dataset["TRANSMISSION"].dropna().unique())
fuel_types = sorted(dataset["FUEL TYPE"].dropna().unique())


def show_prediction():

    st.markdown(
    "<h4 style='margin-bottom:8px;'>Enter Your Vehicle Information</h4>",
    unsafe_allow_html=True
)


    st.subheader("Vehicle Information")

    col1, col2 = st.columns(2)

    with col1:

        make = st.selectbox(
            "Vehicle Make",
            makes
        )

        transmission = st.selectbox(
            "Transmission",
            transmissions
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
            vehicle_classes
        )

        fuel_type = st.selectbox(
            "Fuel Type",
            fuel_types
        )

        engine_size = st.number_input(
            "Engine Size (L)",
            min_value=0.5,
            max_value=10.0,
            value=2.0,
            step=0.1
        )

        fuel_consumption = st.number_input(
            "Fuel Consumption Combined (L/100 km)",
            min_value=1.0,
            max_value=30.0,
            value=8.0,
            step=0.1
        )

    st.divider()

    predict_btn = st.button(
        "🚗 Predict CO₂ Emission",
        use_container_width=True
    )

    if predict_btn:

        input_data = pd.DataFrame({
            "MODEL YEAR": [model_year],
            "MAKE": [make],
            "VEHICLE CLASS": [vehicle_class],
            "ENGINE SIZE (L)": [engine_size],
            "CYLINDERS": [cylinders],
            "TRANSMISSION": [transmission],
            "FUEL TYPE": [fuel_type],
            "FUEL CONSUMPTION COMB (L/100 km)": [fuel_consumption]
        })

        processed_data = preprocessor.transform(input_data)

        prediction = model.predict(processed_data)

        co2 = prediction[0]
        # ---------------- Eco Score ----------------
        #
        # have to improve the ecoscore formula
        eco_score = max(0, min(100, round(100 - (co2 / 6), 1)))

        dense_data = processed_data.toarray()

        shap_values = explainer.shap_values(dense_data)

        if co2 < 180:
            category = "🟢 Low Emission"
            border_color = "#22c55e"

        elif co2 < 300:
            category = "🟡 Moderate Emission"
            border_color = "#f59e0b"

        else:
            category = "🔴 High Emission"
            border_color = "#ef4444"

        # ---------------- Prediction ----------------

        # ---------------- Prediction ----------------

#         st.markdown(
#             f"""
#             <div style="
#                 margin-top:20px;
#                 padding:25px;
#                 border-radius:15px;
#                 border:3px solid {border_color};
#                 text-align:center;
#                 background-color:#1E1E1E;
#             ">
#                 <h3>🚗 Predicted CO₂ Emission</h3>
#                 <h1 style="color:{border_color};">{co2:.2f} g/km</h1>
#                 <h4>{category}</h4>
#             </div>
#             """,
#             unsafe_allow_html=True
# )
        st.success("Prediction Generated Successfully")
        st.divider()

        st.markdown("## 🌱 Eco Score")

        if eco_score >= 80:
            score_message = "🟢 Excellent Fuel Efficiency"

        elif eco_score >= 60:
            score_message = "🟡 Good Fuel Efficiency"

        elif eco_score >= 40:
            score_message = "🟠 Average Fuel Efficiency"

        else:
            score_message = "🔴 Poor Fuel Efficiency"

        col1, col2 = st.columns([1, 3])

        with col1:
            st.metric(
                label="Eco Score",
                value=f"{eco_score}/100"
            )

        with col2:
            st.progress(eco_score / 100)
            st.success(score_message)

        st.divider()

        st.subheader("🧠 AI Explanation")

        feature_names = [
            clean_feature_name(f)
            for f in preprocessor.get_feature_names_out()
        ]

        feature_impacts = pd.DataFrame({
            "Feature": feature_names,
            "Impact": shap_values[0]
        })

        feature_impacts["Absolute"] = feature_impacts["Impact"].abs()

        top_features = (
            feature_impacts
            .sort_values("Absolute", ascending=False)
            .head(5)
        )
        top_feature = top_features.iloc[0]["Feature"]

        st.markdown("#### 🔍 Top Factors")

        for _, row in top_features.iterrows():

            impact = abs(row["Impact"])

            if impact >= 20:
                badge = "🟢 Major Contributor"

            elif impact >= 5:
                badge = "🟡 Moderate Contributor"

            else:
                badge = "⚪ Minor Contributor"

            st.markdown(
                f"""
    **{row['Feature']}**

    {badge}

    ---
    """
            )

        st.markdown("#### 💡 AI Summary")

        major_feature = top_features.iloc[0]["Feature"]

        st.info(
            f"""
    The predicted CO₂ emission is mainly influenced by **{major_feature}**.

    The model also considers fuel type, engine size, transmission,
    vehicle class, cylinders and model year while estimating emissions.

    For a detailed feature-by-feature explanation, open the technical
    analysis below.
    """
        )
        # ---------------- Save Prediction ----------------

        save_prediction(
    user_id=st.session_state.user["id"],

    model_year=model_year,
    make=make,
    vehicle_class=vehicle_class,

    engine_size=engine_size,
    cylinders=cylinders,

    transmission=transmission,
    fuel_type=fuel_type,

    fuel_consumption=fuel_consumption,

    predicted_co2=co2,

    eco_score=eco_score,

    top_influencing_feature=top_feature
)

        base_value = explainer.expected_value

        if hasattr(base_value, "__len__"):
            base_value = float(base_value[0])
        else:
            base_value = float(base_value)

        explanation = shap.Explanation(
            values=shap_values[0],
            base_values=base_value,
            data=dense_data[0],
            feature_names=feature_names
        )

        with st.expander("🔍 Technical Explanation (SHAP)"):

            with st.spinner("Generating explanation..."):

                fig = plt.figure(figsize=(12,6))

                shap.plots.waterfall(
                    explanation,
                    max_display=8,
                    show=False
                )

                st.pyplot(fig)

                plt.close(fig)