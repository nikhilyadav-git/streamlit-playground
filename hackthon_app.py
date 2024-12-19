from datetime import date
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import random

# Load sample data
# Load sample data
def load_data():
    df = pd.read_csv('data/train_pax.csv')
    #df['departure_date'] = pd.to_datetime(df['departure_date'], format='%Y-%m-%d')
    return df

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


# Set the page title and layout
st.set_page_config(page_title="Station App UI", layout="wide")

# Custom CSS to style the app
st.markdown("""
    <style>
        body {
            background-color: #f1f1f1;
            font-family: 'Arial', sans-serif;
        }
        
        .header {
            background: linear-gradient(45deg, #005e99, #009cda);
            color: white;
            padding: 40px;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            border-radius: 10px;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }

        .subheader {
            font-size: 22px;
            font-weight: 600;
            margin-top: 20px;
            color: #333;
        }

        .intro-title {
            font-size: 20px;
            font-weight: 600;
            color: #333;
        }

        .intro-text {
            font-size: 14px;
            color: #555;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        .tab-content {
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-top: 10px;
        }

        .form-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            margin-top: 20px;
        }

        .form-container > div {
            display: flex;
            justify-content: space-between;
            gap: 20px;
        }

        .selectbox, .date-picker {
            width: 48%;
        }

        label {
            font-size: 14px;
            font-weight: 500;
            color: #555;
            margin-bottom: 5px;
        }

        .button-container {
            text-align: center;
        }

        .search-button {
            background-color: #005e99;
            color: white;
            font-size: 16px;
            font-weight: 600;
            padding: 12px 40px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .search-button:hover {
            background-color: #004b80;
        }

        .radio-container {
            padding-left: 20px;
        }

        /* Add extra space between dropdowns and tab container */
        .extra-space {
            margin-bottom: 20px;
        }

    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<div class='header'>Heckathon Station App - 2025</div>", unsafe_allow_html=True)

# Tabs using Streamlit Sidebar
tab = st.sidebar.radio("Choose a Service", ["Passenger", "Trains", "Hotels"])

# Tab content handling
if tab == "Passenger":
    st.markdown("<div class='subheader'>Passenger</div>", unsafe_allow_html=True)

    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    
    # Pax search form
    with st.container():
        travel_date = st.date_input("Select Travel Date", min_value=date.today(), key="date")

        st.title("Passenger Data Visualization")

        # Load data
        df = load_data()
        df['departure_hr'] = pd.to_datetime(df['departure_time'], format='%Y-%m-%d %H:%M:%S').dt.hour
        df['departure_time'] = pd.to_datetime(df['departure_time'], format='%Y-%m-%d %H:%M:%S').dt.time
        df = df.drop(columns=['departure_date','train_number','boarding_station_name_latitude','boarding_station_name_longitude',
                              'arrival_station_name','arrival_station_name_latitude','arrival_station_name_longitude'])

        # Range slider for selecting time range (5 AM to 10 PM)
        start_hour, end_hour = st.slider(
            "Select departure time range",
            min_value=5,  # No leading zero
            max_value=22,
            value=(5, 22),  # No leading zero
            step=1,
        )

        # Filter data based on selected time range
        filtered_data = df[(df['departure_hr'] >= start_hour) & (df['departure_hr'] < end_hour)]
        
        st.write(filtered_data)

        # Group by hour for aggregation
        filtered_data['hour'] = df['departure_hr']

        # Aggregating data by hour (sum of counts)
        agg_data = filtered_data.groupby('hour').agg({
            'pax_EU_count': 'sum',
            'pax_non_EU_count': 'sum',
            'adult_pax_count': 'sum',
            'senior_pax_count': 'sum',
            'youth_pax_count': 'sum',
            'infant_pax_count': 'sum',
            'pax_veg_meal_count': 'sum',
            'pax_non_veg_meal_count': 'sum',
            'pax_diabetic_meal_count': 'sum',
            'pax_vegan_meal_count': 'sum',
            'assistance_required_count': 'sum'
        }).reset_index()

        # Streamlit layout
        st.title("Passenger Count and Meal Data by Hour of Departure")

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plotting multiple lines
        ax.plot(agg_data['hour'], agg_data['pax_EU_count'], label='EU Pax Count', marker='o')
        ax.plot(agg_data['hour'], agg_data['pax_non_EU_count'], label='Non-EU Pax Count', marker='x')
        ax.plot(agg_data['hour'], agg_data['adult_pax_count'], label='Adult Pax Count', marker='^')
        ax.plot(agg_data['hour'], agg_data['senior_pax_count'], label='Senior Pax Count', marker='s')
        ax.plot(agg_data['hour'], agg_data['youth_pax_count'], label='Youth Pax Count', marker='d')
        ax.plot(agg_data['hour'], agg_data['infant_pax_count'], label='Infant Pax Count', marker='p')
        ax.plot(agg_data['hour'], agg_data['pax_veg_meal_count'], label='Veg Meal Count', marker='h')
        ax.plot(agg_data['hour'], agg_data['pax_non_veg_meal_count'], label='Non-Veg Meal Count', marker='*')
        ax.plot(agg_data['hour'], agg_data['pax_diabetic_meal_count'], label='Diabetic Meal Count', marker='v')
        ax.plot(agg_data['hour'], agg_data['pax_vegan_meal_count'], label='Vegan Meal Count', marker='1')
        ax.plot(agg_data['hour'], agg_data['assistance_required_count'], label='Assistance Count', marker='2')

        # Labels and title
        ax.set_title('Passenger Count and Meal Data by Hour of Departure Time')
        ax.set_xlabel('Hour of Departure')
        ax.set_ylabel('Count')
        ax.set_xticks(agg_data['hour'])
        ax.grid(True)
        ax.legend(loc='upper left')

        # Show the plot
        st.pyplot(fig)
        
        # Search Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
elif tab == "Trains":
    st.markdown("<div class='subheader'>Passenger</div>", unsafe_allow_html=True)

    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    
    # Train search form
    with st.container():
        travel_date = st.date_input("Select Travel Date", min_value=date.today(), key="date")

        st.title("Train Data Visualization")

        # Load data
        df = load_data()
        df['departure_time'] = pd.to_datetime(df['departure_time'], format='%Y-%m-%d %H:%M:%S').dt.time
        df['departure_time'] = df['departure_time'].apply(lambda x: x.strftime('%H:%M:%S'))

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
        
        # Search Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='subheader'>Hotels</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='tab-content'>
            <h3 class='intro-title'>Find Your Hotel</h3>
            <p class='intro-text'>Search for hotels at your travel destination. Choose from a wide range of hotels to make your stay comfortable.</p>
        </div>
    """, unsafe_allow_html=True)

    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    

    # Hotel search form
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            destination = st.selectbox("Select Destination", ["Paris", "Brussels", "London", "Amsterdam", "Lille"], key="destination")
        
        with col2:
            checkin_date = st.date_input("Select Check-in Date", min_value=date.today(), key="checkin")
        
        checkout_date = st.date_input("Select Check-out Date", min_value=date.today(), key="checkout")

        # Search Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        if st.button("Search Hotels", key="hotel_button", use_container_width=True):
            st.write(f"Searching for hotels in {destination} from {checkin_date} to {checkout_date}...")
        st.markdown("</div>", unsafe_allow_html=True)