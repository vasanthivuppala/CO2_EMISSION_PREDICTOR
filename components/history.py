import streamlit as st
import pandas as pd
from database import get_user_predictions


def show_history():

    st.title("📊 Previous Predictions")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "prediction"
        st.rerun()

    st.divider()

    predictions = get_user_predictions(
        st.session_state.user["id"]
    )

    if not predictions:
        st.info("No prediction history available.")
        return

    data = []

    for row in predictions:

        data.append({
            "Date & Time": row[2],
            "Model Year": row[3],
            "Make": row[4],
            "Vehicle Class": row[5],
            "Engine Size": row[6],
            "Cylinders": row[7],
            "Transmission": row[8],
            "Fuel Type": row[9],
            "Fuel Consumption": row[10],
            "Predicted CO₂ (g/km)": round(row[11], 2),
            "Eco Score": row[12]
        })

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )