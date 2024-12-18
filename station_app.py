import streamlit as st
import pandas as pd
import pydeck as pdk
import random

# Load sample data
def load_data():
    data = {
        "train_number": [9010, 9020, 9030, 9040, 9050, 9060, 9070, 9080, 9090, 9100, 9110, 9120, 9130, 9140, 9150, 9160, 9170, 9180],
        "departure_date": ["2024-12-25"] * 18,
        "departure_time": [
            "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"
        ],
        "boarding_station_name": ["London St Pancras"] * 18,
        "boarding_station_name_latitude": [51.5304] * 18,
        "boarding_station_name_longitude": [-0.1260] * 18,
        "arrival_station_name": ["Gare du Nord"] * 18,
        "arrival_station_name_latitude": [48.8794] * 18,
        "arrival_station_name_longitude": [2.3557] * 18,
        "pax_EU_count": [150, 160, 155, 170, 180, 190, 185, 160, 175, 165, 155, 145, 150, 160, 170, 180, 185, 190],
        "pax_non_EU_count": [50, 40, 45, 30, 40, 45, 40, 50, 35, 40, 45, 50, 60, 55, 50, 45, 40, 35],
        "adult_pax_count": [100, 110, 105, 120, 125, 130, 120, 110, 115, 110, 105, 95, 100, 110, 120, 130, 135, 140],
        "senior_pax_count": [30, 25, 28, 35, 30, 33, 29, 26, 27, 30, 29, 31, 28, 33, 30, 35, 32, 32],
        "youth_pax_count": [20, 18, 22, 15, 18, 25, 22, 20, 24, 19, 23, 20, 22, 24, 22, 18, 20, 21],
        "infant_pax_count": [5, 7, 6, 10, 12, 12, 7, 8, 6, 6, 7, 9, 10, 8, 10, 12, 9, 9],
        "pax_veg_meal_count": [20, 25, 22, 30, 28, 35, 32, 24, 30, 28, 20, 18, 22, 25, 28, 30, 32, 35],
        "pax_non_veg_meal_count": [80, 85, 78, 90, 92, 95, 88, 82, 85, 80, 75, 72, 77, 82, 85, 90, 92, 95],
        "pax_diabetic_meal_count": [10, 12, 8, 15, 13, 14, 12, 10, 11, 9, 12, 10, 18, 16, 14, 16, 18, 20],
        "pax_vegan_meal_count": [15, 10, 12, 20, 18, 16, 17, 14, 13, 14, 16, 15, 22, 19, 20, 19, 22, 25],
        "assistance_required_count": [5, 4, 6, 7, 9, 10, 8, 5, 6, 7, 4, 3, 6, 7, 8, 9, 6, 7]
    }
    
    return pd.DataFrame(data)

# Function to generate a random RGBA color
def random_color():
    return [random.randint(0, 255) for _ in range(3)] + [random.randint(100, 255)]  # RGB + Alpha (opacity)

# Function to add slight random variation to the coordinates
def add_variation(lat, lon, max_variation=0.01):
    """
    Adds a small random variation to the latitude and longitude.
    This is to prevent all the markers from stacking on the same point.
    """
    lat_variation = random.uniform(-max_variation, max_variation)
    lon_variation = random.uniform(-max_variation, max_variation)
    return lat + lat_variation, lon + lon_variation

# Function to create map visualization with filtered data
def create_map(filtered_data):
    st.write("Map showing departure locations of trains:")
    
    # Add slight random variation to the coordinates to prevent overlap
    filtered_data['boarding_station_name_latitude'], filtered_data['boarding_station_name_longitude'] = zip(
        *filtered_data.apply(lambda row: add_variation(row['boarding_station_name_latitude'], row['boarding_station_name_longitude']), axis=1)
    )
    
    # Ensure that latitude and longitude are float types
    filtered_data['boarding_station_name_latitude'] = filtered_data['boarding_station_name_latitude'].astype(float)
    filtered_data['boarding_station_name_longitude'] = filtered_data['boarding_station_name_longitude'].astype(float)
    
    # Assign random colors to each train
    filtered_data['color'] = [random_color() for _ in range(len(filtered_data))]
    
    # Convert filtered_data to list of dictionaries for pydeck
    data_for_deck = filtered_data.to_dict(orient='records')
    
    # Add data to PyDeck
    view_state = pdk.ViewState(latitude=51.5304, longitude=-0.1260, zoom=5, pitch=50)
    
    # Scatterplot layer with dots for each train
    layer = pdk.Layer(
        "ScatterplotLayer",
        data_for_deck,
        get_position=["boarding_station_name_longitude", "boarding_station_name_latitude"],
        get_radius=500,  # Size of the dots
        get_color="color",  # Use the color column for dot colors
        pickable=True,
        auto_highlight=True
    )
    
    # Tooltip to show train number, departure time, and passenger counts
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Train Number:</b> {train_number}<br><b>Departure Time:</b> {departure_time}<br><b>EU Pax:</b> {pax_EU_count}<br><b>Non-EU Pax:</b> {pax_non_EU_count}<br><b>Adult Pax:</b> {adult_pax_count}<br><b>Senior Pax:</b> {senior_pax_count}<br><b>Youth Pax:</b> {youth_pax_count}<br><b>Infant Pax:</b> {infant_pax_count}",
            "style": {
                "backgroundColor": "white",
                "color": "black",
                "border": "1px solid #ccc",
                "padding": "10px"
            }
        }
    )
    
    st.pydeck_chart(r)

# Main app layout
def main():
    st.title("Train Data Visualization")

    # Load data
    df = load_data()

    # Convert departure_time to datetime for easier filtering
    df["departure_time"] = pd.to_datetime(df["departure_time"], format='%H:%M')

    # Convert departure_time back to HH:MM:SS format (to only show time)
    df["departure_time"] = df["departure_time"].dt.strftime('%H:%M:%S')

    # Range slider for selecting time range (5 AM to 10 PM)
    start_hour, end_hour = st.slider(
        "Select departure time range",
        min_value=5,  # No leading zero
        max_value=22,
        value=(5, 22),  # No leading zero
        step=1,
    )

    # Filter data based on selected time range
    filtered_data = df[(df['departure_time'].apply(lambda x: int(x.split(':')[0])) >= start_hour) & 
                       (df['departure_time'].apply(lambda x: int(x.split(':')[0])) <= end_hour)]
    
    st.write(filtered_data)

    # Create the map with the filtered data
    create_map(filtered_data)

if __name__ == "__main__":
    main()
