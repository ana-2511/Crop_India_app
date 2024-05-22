import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the crop data and the random forest model
crop_data = pd.read_csv("new_Clean_India.csv")
model = joblib.load("random.pkl.gz")
scaler = joblib.load("scaler.pkl")  # Ensure to load the scaler if you used one during training

# Get the list of unique crops from the dataset
crop_list = crop_data['Crop'].unique()

# Define the layout of your app
def main():
    st.title('Best Crop Locations and Yield Prediction App')

    # Add dropdown for user to select crop name
    st.header('Select Crop Name:')
    crop_name = st.selectbox('Crop Name', crop_list)

    # Add a button to show the best locations for the crop
    if st.button('Show Best Locations'):
        # Filter crop data based on user input
        filtered_crop_data = crop_data[crop_data['Crop'] == crop_name]

        # If there is data available for the selected crop, display it
        if not filtered_crop_data.empty:
            # Find the location with the highest yield for the selected crop
            best_location = filtered_crop_data.loc[filtered_crop_data['Yield'].idxmax()]

            # Display information about the best location for the crop
            st.subheader(f'Best Location for {crop_name}:')
            st.write(f"State: {best_location['State_Name']}")
            st.write(f"District: {best_location['District_Name']}")
            st.write(f"Season: {best_location['Season']}")
            st.write(f"Area: {best_location['Area']}")
            st.write(f"Production: {best_location['Production']}")
            st.write(f"Yield: {best_location['Yield']}")
        else:
            st.warning(f'No data available for {crop_name}.')

    # Add input fields for user to enter production and area for yield calculation
    st.header('Calculate Yield:')
    production_calc = st.number_input('Production for Calculation', min_value=0.0)
    area_calc = st.number_input('Area for Calculation', min_value=0.0)

    # Add a button to calculate yield
    if st.button('Calculate Yield'):
        if area_calc > 0:
            yield_value = production_calc / area_calc
            st.success(f'Calculated Yield: {yield_value}')
        else:
            st.error('Area must be greater than 0 to calculate yield.')

# Run the app
if __name__ == '__main__':
    main()
