from geopy.geocoders import Nominatim

def get_hospital_address(hospital_name):
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="hospital_address")
    
    # Search for the hospital by name
    location = geolocator.geocode(hospital_name, addressdetails=True, limit=1)
    
    # Extract and return the hospital address
    if location:
        hospital_address = location.address
        return hospital_address
    else:
        return None

# Example usage:
hospital_name = "hospital_name_here"  # Replace with the name of the hospital
hospital_address = get_hospital_address(hospital_name)
if hospital_address:
    print(f"The address of {hospital_name} is: {hospital_address}")
else:
    print(f"No address found for {hospital_name}.")
