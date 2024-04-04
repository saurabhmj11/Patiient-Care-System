import numpy as np
import pandas as pd
import streamlit as st
import pickle
from geolocation import get_geolocation  # Import the get_geolocation function from geolocation.py
from geopy.geocoders import Nominatim

# Set page configuration
st.set_page_config(page_title="Patient Care Classification System", page_icon=":hospital:")

# Function to get the address of the nearest hospital or doctor based on user's location
def get_nearest_hospital_address(user_location):
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="hospital_address")
    
    # Search for the nearest hospital
    location = geolocator.reverse(user_location, addressdetails=True)
    
    # Extract and return the hospital address
    if location:
        hospital_address = location.address
        return hospital_address
    else:
        return None

# Define the full absolute file path to the model file
model_file_path = "https://github.com/saurabhmj11/Patiient-Care-System/blob/1e45138f788ab83a1d9d48e3c188cee09160a2e8/random_forest_model.pkl"

# Load the trained Random Forest model from the pickle file
with open(model_file_path, "rb") as model_file:
    rf_model = pickle.load(model_file)

# Set dark theme
st.markdown(
    """
    <style>
    body {
        color: #f8f9fa;
        background-color: #272727;
    }
    .stNumberInput > div > div > input {
        color: #f8f9fa;
        background-color: #343a40;
        border-color: #6c757d;
    }
    .stTextInput > div > div > input {
        color: #f8f9fa;
        background-color: #343a40;
        border-color: #6c757d;
    }
    .stButton>button {
        color: #f8f9fa;
        background-color: #007bff;
        border-color: #007bff;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.title("Patient Care Classification System")
st.write("Predict whether home care or hospitalization is required based on patient's data.")

# User input section
st.sidebar.subheader("Enter Patient's Data")
st_HAEMATOCRIT = st.sidebar.number_input("HAEMATOCRIT Value", format="%f", step=0.1)
st_HAEMOGLOBINS = st.sidebar.number_input("HAEMOGLOBINS Value", format="%f", step=0.1)
st_ERYTHROCYTE = st.sidebar.number_input("ERYTHROCYTE Value", format="%f", step=0.1)
st_LEUCOCYTE = st.sidebar.number_input("LEUCOCYTE Value", format="%f", step=0.1)
st_THROMBOCYTE = st.sidebar.number_input("THROMBOCYTE Value", format="%f", step=0.1)
st_MCH = st.sidebar.number_input("MCH Value", format="%f", step=0.1)
st_MCHC = st.sidebar.number_input("MCHC Value", format="%f", step=0.1)
st_MCV = st.sidebar.number_input("MCV Value", format="%f", step=0.1)
st_AGE = st.sidebar.number_input("AGE Value", format="%d", min_value=0)
st_SEX = st.sidebar.radio("SEX", options=["Male", "Female"])

# Convert SEX to numerical value
sex_mapping = {"Male": 1, "Female": 0}
st_SEX_numeric = sex_mapping[st_SEX]

# User data
user_data = {
    "HAEMATOCRIT": st_HAEMATOCRIT,
    "HAEMOGLOBINS": st_HAEMOGLOBINS,
    "ERYTHROCYTE": st_ERYTHROCYTE,
    "LEUCOCYTE": st_LEUCOCYTE,
    "THROMBOCYTE": st_THROMBOCYTE,
    "MCH": st_MCH,
    "MCHC": st_MCHC,
    "MCV": st_MCV,
    "AGE": st_AGE,
    "SEX": st_SEX_numeric,
}

# Display user input summary
st.sidebar.subheader("User Input Summary")
st.sidebar.write(pd.DataFrame(user_data, index=["Value"]))

# Make predictions using the loaded Random Forest model
user_df = pd.DataFrame(user_data, index=[0])
rf_predict_user_data = rf_model.predict(user_df)

# Determine the action to be taken based on the prediction
if rf_predict_user_data == 0:
    care = "Out Care (Home Care) Required"
else:
    care = "In Care (Hospitalization) Required"

# Display the prediction result
st.subheader("Prediction Result")
if rf_predict_user_data == 0:
    st.success(care)
else:
    st.error(care)

# Get the user's location and display nearest hospital address if hospitalization is required
if rf_predict_user_data == 1:
    st.sidebar.subheader("Enter Your Address")
    user_address = st.sidebar.text_input("Address")
    if user_address:
        geolocator = Nominatim(user_agent="hospital_address")
        user_location = geolocator.geocode(user_address)
        if user_location:
            user_latitude = user_location.latitude
            user_longitude = user_location.longitude
            user_location_str = f"Latitude: {user_latitude}, Longitude: {user_longitude}"
            st.sidebar.write("Your Location:", user_location_str)
            hospital_address = get_nearest_hospital_address((user_latitude, user_longitude))
            if hospital_address:
                st.sidebar.subheader("Nearest Hospital Address")
                st.sidebar.write(hospital_address)
            else:
                st.sidebar.error("No hospital found near your location.")

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        background-color: #272727;
        color: #f8f9fa;
        padding: 10px 0;
    }
    </style>
    <div class="footer">
        Developed by Saurabh Lokhande
    </div>
    """,
    unsafe_allow_html=True
)
