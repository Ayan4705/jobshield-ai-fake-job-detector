import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

from backend.database import (
    init_db,
    save_history,
    get_history,
    get_all_history,
    is_user_admin
)

from backend.auth import (
    register,
    login
)

from backend.hybrid_engine import (
    rule_engine,
    hybrid_score
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Advanced Fake Job Detector",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🛡️ Advanced Fake Job Detector")
st.markdown(
    "AI + Rule Based Fraud Detection for Job Postings"
)

# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_db()

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_models():

    model = joblib.load(
        "models/trained_model.pkl"
    )

    vectorizer = joblib.load(
        "models/vectorizer.pkl"
    )

    return model, vectorizer


model, vectorizer = load_models()

# =========================================================
# SIDEBAR MENU
# =========================================================

menu = ["Home","Login", "Register"]

choice = st.sidebar.selectbox(
    "Navigation",
    menu
)

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================================================
# HOME PAGE
# =========================================================

if choice == "Home":

    st.title("🛡️ JobShield AI")
    st.subheader("Fake Job Detection System")

    st.image(
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40",
        width=350
    )

    st.markdown("""
    ### Welcome to JobShield AI

    JobShield AI is an intelligent fake job detection system that helps
    users identify fraudulent job postings using Machine Learning and
    Rule-Based Analysis.

    ### Features
    ✅ User Registration & Login

    ✅ Fake Job Detection

    ✅ Machine Learning Prediction

    ✅ Hybrid Fraud Analysis

    ✅ Prediction History

    ✅ Admin Dashboard & Analytics

    ### Project Objective
    To protect job seekers from employment scams and promote safe online recruitment.
    """)

# =========================================================
# REGISTER PAGE
# =========================================================

if choice == "Register":

    st.subheader("📝 Create Account")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        if username == "" or password == "":

            st.warning(
                "⚠️ Please fill all fields"
            )

        else:

            success = register(username, password)

            if success:
                st.success(
                    "✅ Registered Successfully"
                )

            else:
                st.error(
                    "❌ Username already exists"
                )

# =========================================================
# LOGIN PAGE
# =========================================================

elif choice == "Login":

    # =============================================
    # LOGIN FORM
    # =============================================

    if not st.session_state.logged_in:

        st.subheader("🔐 Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if login(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(
                    "✅ Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Credentials"
                )

    # =============================================
    # AFTER LOGIN
    # =============================================

    else:

        username = st.session_state.username

        st.success(
            f"✅ Welcome {username}"
        )

        # =============================================
        # LOGOUT BUTTON
        # =============================================

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.rerun()

        # =============================================
        # ADMIN CHECK
        # =============================================

        is_admin = is_user_admin(username)

        # =============================================
        # ADMIN PANEL
        # =============================================

        if is_admin:

            st.subheader(
                "👑 Admin Dashboard"
            )

            all_history = get_all_history()

            if all_history:

                df_admin = pd.DataFrame(
                    all_history,
                    columns=[
                        "Username",
                        "Job Text",
                        "ML Score",
                        "Rule Score",
                        "Hybrid Score",
                        "Verdict"
                    ]
                )

                st.dataframe(
                    df_admin,
                    use_container_width=True
                )

                fig1 = px.pie(
                    df_admin,
                    names="Verdict",
                    title="All User Verdict Distribution"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

                fig2 = px.bar(
                    df_admin,
                    x="Username",
                    y="Hybrid Score",
                    color="Verdict",
                    title="User Analysis Overview"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

        # =============================================
        # USER ANALYSIS
        # =============================================

        st.subheader(
            "📄 Job Description Analysis"
        )

        job_text = st.text_area(
            "Paste Job Description Here",
            height=250
        )

        if st.button("Analyze Job"):

            if job_text.strip() == "":

                st.warning(
                    "⚠️ Please paste a job description"
                )

            elif len(job_text) > 10000:

                st.warning(
                    "⚠️ Job description too long. "
                    "Please limit to 10,000 characters."
                )

            else:

                with st.spinner(
                    "Analyzing Job Posting..."
                ):

                    # ML Prediction
                    vec = vectorizer.transform(
                        [job_text]
                    )

                    ml_prob = model.predict_proba(
                        vec
                    )[0][1]

                    # Rule Engine
                    rule_score_value, reasons = (
                        rule_engine(job_text)
                    )

                    # Hybrid Score
                    final = hybrid_score(
                        ml_prob,
                        rule_score_value
                    )

                    # Verdict
                    if final >= 75:
                        verdict = "Fake"

                    elif final >= 40:
                        verdict = "Suspicious"

                    else:
                        verdict = "Real"

                    # Save History
                    save_history(
                        username,
                        job_text,
                        ml_prob * 100,
                        rule_score_value,
                        final,
                        verdict
                    )

                # =====================================
                # RESULTS
                # =====================================

                st.subheader(
                    "📊 Analysis Results"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "ML Probability",
                        f"{ml_prob * 100:.2f}%"
                    )

                with col2:
                    st.metric(
                        "Rule Score",
                        f"{rule_score_value:.2f}%"
                    )

                with col3:
                    st.metric(
                        "Hybrid Score",
                        f"{final:.2f}%"
                    )

                # Verdict
                st.subheader(
                    "🧠 Final Verdict"
                )

                if verdict == "Fake":

                    st.error(
                        "🚨 Highly Suspicious / Fake Job"
                    )

                elif verdict == "Suspicious":

                    st.warning(
                        "⚠️ Potentially Suspicious Job"
                    )

                else:

                    st.success(
                        "✅ Likely Genuine Job Posting"
                    )

                # Explainability
                st.subheader(
                    "🔍 Explainability"
                )

                if reasons:

                    for reason in reasons:
                        st.warning(reason)

                else:

                    st.success(
                        "No suspicious patterns detected"
                    )

                # ML Top Keywords
                st.markdown("** Top ML Keywords Driving This Score:**")

                feature_names = vectorizer.get_feature_names_out()
                importances = model.feature_importances_
                vec_array = vectorizer.transform([job_text]).toarray()[0]

                # Only show features present in this job text
                present_indices = [
                    i for i, v in enumerate(vec_array) if v > 0
                ]
                present_indices_sorted = sorted(
                    present_indices,
                    key=lambda i: importances[i],
                    reverse=True
                )[:10]

                if present_indices_sorted:
                    for i in present_indices_sorted:
                        st.info(
                            f"🔑 `{feature_names[i]}` "
                            f"— importance: "
                            f"{importances[i]:.4f}"
                        )
                else:
                    st.info("No significant keywords found.")

        # =====================================
        # USER HISTORY (always visible)
        # =====================================

        st.subheader(
            "🗂️ Previous Analysis History"
        )

        history = get_history(username)

        if history:

            for row in history:

                df_history = pd.DataFrame(
                    history,
                    columns=[
                        "Job Text",
                        "ML Score",
                        "Rule Score",
                        "Hybrid Score",
                        "Verdict"
                    ]
                )

                df_history["Job Text"] = (
                    df_history["Job Text"].str[:60] + "..."
                )

                st.dataframe(
                    df_history,
                    use_container_width=True
                )

        else:

            st.info(
                "No history found"
            )

        # =====================================
        # DASHBOARD (always visible)
        # =====================================

        if history:

            st.subheader(
                "📊 Dashboard"
            )

            df_history = pd.DataFrame(
                history,
                columns=[
                    "Job Text",
                    "ML Score",
                    "Rule Score",
                    "Hybrid Score",
                    "Verdict"
                ]
            )

            fig3 = px.pie(
                df_history,
                names="Verdict",
                title="Fake vs Real Jobs"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

            fig4 = px.bar(
                df_history,
                x="Verdict",
                y="Hybrid Score",
                color="Verdict",
                title="Verdict Distribution"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )