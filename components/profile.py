import streamlit as st

def show_profile():

    left, middle, right = st.columns([6, 2, 1])

    with left:
        st.markdown(
            """
            <h2 style='margin-top:5px;'>
                🚗 CO₂ Emission Predictor
            </h2>
            """,
            unsafe_allow_html=True
        )

    with middle:
        st.markdown(
            f"""
            <div style="text-align:right; padding-top:12px; font-size:18px;">
                👤 <b>{st.session_state.user['name']}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.show_signup = False
            st.rerun()
            