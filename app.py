import streamlit as st
from components.history import show_history
from components.prediction import show_prediction
from components.profile import show_profile
from auth import signup_user, login_user
from database import create_tables

st.set_page_config(
    page_title="CO₂ Emission Predictor",
    page_icon="🚗",
    layout="wide"
)
st.markdown("""
<style>

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

/* Hide Streamlit header */
header {
    visibility: hidden;
}

/* Remove top padding */
.block-container{
    padding-top:1rem;
}

</style>
""", unsafe_allow_html=True)

create_tables()

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False


# -------------------- LOGIN / SIGNUP --------------------
if not st.session_state.logged_in:

    if not st.session_state.show_signup:

        st.title("🔐 Login")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login", use_container_width=True):

            success, result = login_user(email, password)

            if success:
                st.session_state.logged_in = True
                st.session_state.user = result
                st.success("Login Successful!")
                st.rerun()

            else:
                st.error(result)

        st.write("---")
        st.write("Don't have an account?")

        if st.button("Create Account"):
            st.session_state.show_signup = True
            st.rerun()

    else:

        st.title("📝 Create Account")

        name = st.text_input("Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Sign Up", use_container_width=True):

            success, message = signup_user(
                name,
                email,
                password
            )

            if success:
                st.success(message)

            else:
                st.error(message)

        st.write("---")
        st.write("Already have an account?")

        if st.button("Back to Login"):
            st.session_state.show_signup = False
            st.rerun()


# -------------------- MAIN APP --------------------
else:

    # -------------------- Navigation --------------------

    if "page" not in st.session_state:
        st.session_state.page = "prediction"

    show_profile()

    st.divider()

    if st.session_state.page == "prediction":
        show_prediction()

    elif st.session_state.page == "history":
        show_history()