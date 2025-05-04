import streamlit as st
from pathlib import Path
import pandas as pd
import markdown
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

st.set_page_config(page_title="JB Housing Empire AI", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: cyan;'>JB Housing Empire AI System</h1>",
    unsafe_allow_html=True
)
st.image("logo.jpg", width=200)

page = st.sidebar.selectbox("Navigation", [
    "Home", "Dashboard", "Lead Intake", "Deal Analyzer",
    "Calculators", "Script Generator", "LOI Builder", "Empire Manual"
])

api_key = os.getenv("OPENAI_API_KEY")
model_choice = "gpt-3.5-turbo"

if page == "Home":
    st.header("Welcome to JB Housing Empire AI System")
    st.markdown("### Modules:")
    st.write("- Lead Scraping & CRM")
    st.write("- Full Deal Analyzer")
    st.write("- GPT-Powered Script Builder")
    st.write("- LOI Templates")
    st.write("- Multifamily Underwriting")
    st.write("- Empire Training Manual")

elif page == "Dashboard":
    st.header("📊 KPI Dashboard")
    try:
        with open("KPI.json", "r") as kpi_file:
            kpi_data = json.load(kpi_file)
            st.write("**Total Leads:**", kpi_data.get("totalLeads", 0))
            st.write("**Response Rate:**", f"{kpi_data.get('responseRate', 0)}%")
            st.write("**Conversions:**", kpi_data.get("conversions", 0))
            st.write("**Cash Flow:**", f"${kpi_data.get('cashFlow', 0)}")
            st.write("**ROI:**", f"{kpi_data.get('roi', 0)}%")
    except Exception as e:
        st.error(f"Unable to load KPI data: {e}")

elif page == "Lead Intake":
    st.header("📁 Deal Flow Leads")
    uploaded = st.file_uploader("Upload deal_flow.csv", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df)

elif page == "Deal Analyzer":
    st.header("📈 Deal Analyzer")
    address = st.text_input("Enter Property Address")
    if st.button("Analyze with GPT"):
        if not api_key:
            st.warning("API Key not found. Please set OPENAI_API_KEY in .env")
        else:
            try:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": "You are a real estate underwriting assistant."},
                        {"role": "user", "content": f"/analyze {address}"}
                    ]
                )
                st.success("GPT Analysis:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Calculators":
    st.header("🧮 Deal Calculators")
    st.info("Use other tabs for full calculators (SubTo, Seller Finance, etc.)")

elif page == "Script Generator":
    st.header("🤖 GPT Script Generator")
    deal_type = st.selectbox("Deal Type", ["SubTo", "Wrap", "Seller Finance", "Cash", "Hybrid"])
    if st.button("Generate Script with GPT"):
        if not api_key:
            st.warning("API Key not found. Please set OPENAI_API_KEY in .env")
        else:
            try:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": "You generate real estate negotiation scripts in a 5x5 format."},
                        {"role": "user", "content": f"/script {deal_type}"}
                    ]
                )
                st.success("GPT Script:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "LOI Builder":
    st.header("📄 LOI Generator")
    structure = st.selectbox("Deal Structure", ["SubTo", "Seller Finance", "Wrap", "Hybrid"])
    name = st.text_input("Seller Name")
    price = st.number_input("Offer Price")
    if st.button("Generate LOI with GPT"):
        if not api_key:
            st.warning("API Key not found. Please set OPENAI_API_KEY in .env")
        else:
            try:
                client = openai.OpenAI(api_key=api_key)
                prompt = f"/loi {structure}\nSeller: {name}\nPrice: ${price}"
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": "You write formal real estate Letters of Intent."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("GPT LOI:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Empire Manual":
    st.header("📘 Empire Manual")
    try:
        with open("empire_manual.md", "r") as md_file:
            st.markdown(md_file.read())
    except FileNotFoundError:
        st.error("Manual file not found.")
