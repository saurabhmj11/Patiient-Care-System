# Patient Care Classification System

This repository contains a Streamlit web application for predicting whether home care or hospitalization is required based on patient's data. The application utilizes a trained Random Forest model for classification and geolocation services to find the nearest hospital address.

## Features

- Predicts whether home care or hospitalization is required based on patient's data.
- Provides address of the nearest hospital or doctor if hospitalization is required.

## Installation

1. Clone this repository:

git clone https://github.com/your_username/patient-care-classification-system.git

markdown
Copy code

2. Install the required dependencies:

pip install -r requirements.txt

markdown
Copy code

3. Run the Streamlit app:

streamlit run app.py

markdown
Copy code

## Usage

- After running the Streamlit app, input the patient's data in the sidebar.
- The application will predict whether home care or hospitalization is required based on the input data.
- If hospitalization is required, enter the patient's address in the sidebar to find the nearest hospital.

## Dependencies

- Python 3.x
- Streamlit
- Geopy

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for detail
