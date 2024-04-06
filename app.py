import streamlit as st
import pandas as pd
import base64

from joblib import load

# Load the trained Random Forest model
rf_model = load("random_forest_model.joblib")


# Define function to predict care type
def predict_care(user_data):
    # Remove "Patient's Name" and "Patient's Address" from user data
    user_data.pop("Patient's Name", None)
    user_data.pop("Patient's Address", None)
    
    user_df = pd.DataFrame(user_data, index=[0])
    prediction = rf_model.predict(user_df)[0]
    return "In Care (Hospitalization) Required" if prediction == 1 else "Out Care (Home Care) Required"

# Define function to create a download link for DataFrame as CSV
def download_csv(dataframe, filename):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download Result</a>'
    return href

# Define UI layout and style
st.set_page_config(
    page_title="Patient Care Classification System",
    page_icon=":hospital:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
"""
<style>
body {
    font-family: Arial, sans-serif;
    color: #333333;
    background-color: #f8f9fa;
}
.sidebar .sidebar-content {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.sidebar .sidebar-content:hover {
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}
.sidebar .sidebar-content::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 100%);
    z-index: 1;
    pointer-events: none;
    transition: all 0.3s ease;
    border-radius: 10px;
}
.sidebar .sidebar-content:hover::before {
    height: 150%;
}
.sidebar .sidebar-content > div {
    position: relative;
    z-index: 2;
}
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #007bff;
    color: #ffffff;
    text-align: center;
    padding: 10px 0;
}
.logo {
    display: flex;
    align-items: center;
}
.logo img {
    width: 50px;
    height: auto;
    margin-right: 10px;
}
.title {
    color: #007bff;
}
</style>
"""
, unsafe_allow_html=True)

# Main content
st.title("Patient Care Classification System")
st.write("Predict whether home care or hospitalization is required based on patient's data.")

# Sidebar for user input
st.sidebar.header("Enter Patient's Data")

with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)

patient_name = st.text_input("Patient's Name")
patient_address = st.text_area("Patient's Address")

haematocrit = st.number_input("HAEMATOCRIT Value", format="%f", step=0.1)
haemoglobins = st.number_input("HAEMOGLOBINS Value", format="%f", step=0.1)
erythrocyte = st.number_input("ERYTHROCYTE Value", format="%f", step=0.1)
leucocyte = st.number_input("LEUCOCYTE Value", format="%f", step=0.1)
thrombocyte = st.number_input("THROMBOCYTE Value", format="%f", step=0.1)
mch = st.number_input("MCH Value", format="%f", step=0.1)
mchc = st.number_input("MCHC Value", format="%f", step=0.1)
mcv = st.number_input("MCV Value", format="%f", step=0.1)
age = st.number_input("AGE Value", format="%d", min_value=0)
sex = st.selectbox("SEX", options=["Male", "Female"])

# Predict button
if st.button("Predict"):
    user_data = {
        "HAEMATOCRIT": haematocrit,
        "HAEMOGLOBINS": haemoglobins,
        "ERYTHROCYTE": erythrocyte,
        "LEUCOCYTE": leucocyte,
        "THROMBOCYTE": thrombocyte,
        "MCH": mch,
        "MCHC": mchc,
        "MCV": mcv,
        "AGE": age,
        "SEX": 1 if sex == "Male" else 0
    }
    prediction = predict_care(user_data)
    result_df = pd.DataFrame(user_data, index=[0])
    result_df["Prediction"] = prediction
    st.success(f"Prediction: {prediction}")

    # Download button for result
    st.markdown(download_csv(result_df, "prediction_result"), unsafe_allow_html=True)

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
"""
<div class="footer">
    <p>Made with ❤️ by Saurabh Lokhande</p>
</div>
"""
, unsafe_allow_html=True)
