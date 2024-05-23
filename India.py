import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the crop data and the random forest model
crop_data = pd.read_csv("new_Clean_India.csv")
model = joblib.load("random.pkl.gz")
scaler = joblib.load("scaler.pkl")

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
            st.write(f"Area: {best_location['Area']} Hectares")
            st.write(f"Production: {best_location['Production']} Tonnes")
            st.write(f"Yield: {best_location['Yield']} Tonnes per Hectare")
        else:
            st.warning(f'No data available for {crop_name}.')

    # Add input fields for user to enter production and area for yield calculation
    st.header('Calculate Yield:')
    production_calc = st.number_input('Production for Calculation', min_value=0.0)
    production_unit = st.selectbox('Production Unit', ['Tonnes', 'Quintal'])
    area_calc = st.number_input('Area for Calculation', min_value=0.0)
    area_unit = st.selectbox('Area Unit', ['Hectare', 'Acre'])

    # Add a button to calculate yield
    if st.button('Calculate Yield'):
        if area_calc > 0:
            # Convert units to standard units (Hectares for area, Tonnes for production)
            if area_unit == "Acre":
                area_in_hectares = area_calc * 0.404686
            else:
                area_in_hectares = area_calc

            if production_unit == "Quintal":
                production_in_tonnes = production_calc * 0.1
            else:
                production_in_tonnes = production_calc

            yield_value = production_in_tonnes / area_in_hectares

            # Determine the correct unit for display
            if production_unit == "Tonnes" and area_unit == "Hectare":
                unit = "Tonnes per Hectare"
                display_yield_value = yield_value
            elif production_unit == "Quintal" and area_unit == "Acre":
                unit = "Quintal per Acre"
                # Convert Tonnes per Hectare to Quintal per Acre
                display_yield_value = yield_value * (10 / 2.47105)
            else:
                unit = "Unknown unit"
                display_yield_value = yield_value

            st.success(f'Calculated Yield: {display_yield_value:.2f} {unit}')
        else:
            st.error('Area must be greater than 0 to calculate yield.')

# Run the app
if __name__ == '__main__':
    main()
