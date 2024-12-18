import streamlit as st
from datetime import date

# Set the page title and layout
st.set_page_config(page_title="Travel UI", layout="wide")

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
st.markdown("<div class='header'>Travel System</div>", unsafe_allow_html=True)

# Tabs using Streamlit Sidebar
tab = st.sidebar.radio("Choose a Service", ["Trains", "Trains + Hotels", "Hotels"])

# Tab content handling
if tab == "Trains":
    st.markdown("<div class='subheader'>Trains</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='tab-content'>
            <h3 class='intro-title'>Find Your Train</h3>
            <p class='intro-text'>Book your train tickets to various destinations. Simply enter your departure and arrival details, select your preferred train, and confirm your booking.</p>
        </div>
    """, unsafe_allow_html=True)

    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    

    # Train search form
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            departure_station = st.selectbox("Select Departure Station", ["London", "Paris", "Brussels", "Amsterdam", "Lille"], key="departure")
        
        with col2:
            arrival_station = st.selectbox("Select Arrival Station", ["London", "Paris", "Brussels", "Amsterdam", "Lille"], key="arrival")

        travel_date = st.date_input("Select Travel Date", min_value=date.today(), key="date")
        
        # Search Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        if st.button("Search Trains", key="train_button", use_container_width=True):
            st.write(f"Searching trains from {departure_station} to {arrival_station} on {travel_date}...")
        st.markdown("</div>", unsafe_allow_html=True)

elif tab == "Trains + Hotels":
    st.markdown("<div class='subheader'>Trains + Hotels</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='tab-content'>
            <h3 class='intro-title'>Book Your Train and Hotel</h3>
            <p class='intro-text'>Book a combined package for your train journey and hotel stay at your destination. Choose a departure station, arrival station, and preferred hotel options.</p>
        </div>
    """, unsafe_allow_html=True)

    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    

    # Train and hotel search form
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            departure_station = st.selectbox("Select Departure Station", ["London", "Paris", "Brussels", "Amsterdam", "Lille"], key="departure")
        
        with col2:
            arrival_station = st.selectbox("Select Arrival Station", ["London", "Paris", "Brussels", "Amsterdam", "Lille"], key="arrival")

        travel_date = st.date_input("Select Travel Date", min_value=date.today(), key="date")
        hotel = st.selectbox("Select Hotel", ["Hotel A", "Hotel B", "Hotel C", "Hotel D", "Hotel E"], key="hotel")
        
        # Search Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        if st.button("Search Trains + Hotels", key="train_hotel_button", use_container_width=True):
            st.write(f"Searching for trains from {departure_station} to {arrival_station} on {travel_date} and hotels like {hotel}...")
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