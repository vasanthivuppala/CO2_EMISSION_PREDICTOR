import streamlit as st


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.show_signup = False
    st.session_state.page = "prediction"
    st.rerun()


def show_profile():

    left, right = st.columns([8, 2])

    with left:
        st.markdown(
            """
            <h2 style='margin-top:5px;'>
                🚗 CO₂ Emission Predictor
            </h2>
            """,
            unsafe_allow_html=True
        )

    with right:
        with st.popover(f"👤 {st.session_state.user['name']}"):

            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.page = "prediction"
                st.rerun()

            if st.button("📊 Previous Predictions", use_container_width=True):
                st.session_state.page = "history"
                st.rerun()

            st.divider()

            if st.button("🚪 Logout", use_container_width=True):
                logout()