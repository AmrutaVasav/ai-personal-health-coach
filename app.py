import streamlit as st
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Personal Health Coach",
    page_icon="💪",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #1f4037, #99f2c8);
}
h1, h2, h3 {
    color: white;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #ff1a1a;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #111;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏋️ Navigation")
page = st.sidebar.radio("Go to", ["Home", "AI Insights"])

# ---------------- HOME PAGE ----------------
if page == "Home":

    st.title("💪 AI Personal Health Coach")
    st.write("### Your AI-powered fitness analytics dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Calories Target", "2200 kcal")
    col2.metric("👟 Steps Goal", "10,000")
    col3.metric("😴 Sleep Goal", "8 hrs")

    st.divider()

    st.subheader("📂 Upload Your Health Data")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        key="home_upload"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.success("✅ File Uploaded Successfully!")

        st.subheader("📊 Data Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Health Trends")

        col1, col2 = st.columns(2)

        if "Steps" in df.columns:
            fig1, ax1 = plt.subplots()
            ax1.plot(df["Steps"])
            ax1.set_title("Steps Trend")
            col1.pyplot(fig1)

        if "Calories" in df.columns:
            fig2, ax2 = plt.subplots()
            ax2.plot(df["Calories"])
            ax2.set_title("Calories Trend")
            col2.pyplot(fig2)

# ---------------- AI INSIGHTS PAGE ----------------
elif page == "AI Insights":

    st.title("🤖 AI Health Recommendations")

    uploaded_file = st.file_uploader(
        "Upload CSV for AI Analysis",
        type=["csv"],
        key="ai_upload"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        summary = df.describe().to_string()

        api_key = os.getenv("GROQ_API_KEY")

        if api_key:
            with st.spinner("Generating AI insights..."):

                prompt = f"""
                Based on this health data summary:
                {summary}

                Provide:
                - Fitness improvement suggestions
                - Diet recommendations
                - Sleep optimization tips
                - Weekly performance feedback
                """

                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                data = {
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data
                )

                result = response.json()
                advice = result["choices"][0]["message"]["content"]

                st.success("✅ AI Recommendations Ready!")
                st.write(advice)

        else:
            st.error("⚠ Please set GROQ_API_KEY in environment variables.")