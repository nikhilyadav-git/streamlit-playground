from datetime import date
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import random
import seaborn as sns
import folium
from streamlit_folium import st_folium
import hashlib
import plotly.express as px

# Load sample data
def load_train_data():
    df = pd.read_csv('data/train.csv')
    return df

# Helper functions
# Function to generate a random RGBA color
def random_color():
    return [random.randint(0, 100) for _ in range(3)] + [random.randint(100, 255)]  # RGB + Alpha (opacity)

# Function to add slight random variation to the coordinates
def add_variation(lat, lon, max_variation=0.001):
    """
    Adds a small random variation to the latitude and longitude.
    This prevents all markers from stacking on the same point.
    """
    lat_variation = random.uniform(-max_variation, max_variation)
    lon_variation = random.uniform(-max_variation, max_variation)
    return lat + lat_variation, lon + lon_variation

# Create a hash of the DataFrame to detect changes
def dataframe_hash(df):
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()

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
st.markdown("<div class='header'>Hackathon Station App - 2024</div>", unsafe_allow_html=True)

# Tabs using Streamlit Sidebar
tab = st.sidebar.radio("Choose a Service", ["Trains", "Passenger", "Hotel", "Station Bot"])

# Tab content handling
if tab == "Trains":
    st.markdown("<div class='subheader'>Trains</div>", unsafe_allow_html=True)
    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    # Train search form
    with st.container():
        st.title("Train Data Visualization")
        # Load data
        df = load_train_data()
        df = df[['train_no','scheduled_dt','route','carrier','eq_code','set_no','dep_delay','arr_delay','station','country','latitude','longitude','zoom','hr','group','assistance','duty','premier','plus','standard','wheelchair_companion','wheelchair','senior','adult','youth','child','guide_dog']]
        #Travel Date
        df['scheduled_dt'] = pd.to_datetime(df['scheduled_dt']).dt.date
        min_date = df['scheduled_dt'].min()
        max_date = df['scheduled_dt'].max()
        travel_date = st.date_input("Select Travel Date",
                                    min_value=min_date,
                                    max_value=max_date,
                                    key="travel_date")
        #Boarding Station
        boarding_station = df['station'].unique()
        # Create the dropdown
        selected_station = st.selectbox('Select A Boarding Station', boarding_station)
        # Range slider for selecting time range (5 AM to 10 PM)
        start_hour, end_hour = st.slider(
            "Select departure time range",
            min_value=5,  # No leading zero
            max_value=22,
            value=(5, 22),  # No leading zero
            step=1,
        )
        # Filter data based on selected time range
        filtered_data = df[((df['hr'] >= start_hour) & (df['hr'] < end_hour)) & (df['station'] == selected_station) & (df['scheduled_dt'] == travel_date)]
        filtered_data.replace('-', None, inplace=True)
        # Replace None or NaN values with 0
        filtered_data = filtered_data.fillna(0)
        st.write(filtered_data)
        # Title of the Dashboard
        st.title("Train Data Dashboard")
        col1, col2 = st.columns(2)
        # 1. Route Plot
        with col1:
            st.subheader("1. Route By Hour")
            route_counts = filtered_data['route'].value_counts()
            fig_route = plt.figure(figsize=(8, 6))
            plt.pie(route_counts, labels=route_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(route_counts)))
            plt.title("Route Distribution")
            st.pyplot(fig_route)
        # 2. Carrier Plot
        with col2:
            st.subheader("2. Carrier By Hour")
            carrier_counts = filtered_data['carrier'].value_counts()
            fig_carrier = plt.figure(figsize=(8, 6))
            plt.pie(carrier_counts, labels=carrier_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(carrier_counts)))
            plt.title("Carrier Distribution")
            st.pyplot(fig_carrier)
        # Empty space for better alignment between rows
        st.empty()
        # 3. EQ_Code Plot
        with col1:
            st.subheader("3. Equipment Type By Hour")
            eq_code_counts = filtered_data['eq_code'].value_counts()
            fig_eq_code = plt.figure(figsize=(8, 6))
            plt.pie(eq_code_counts, labels=eq_code_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set1", len(eq_code_counts)))
            plt.title("Equipment Type Distribution")
            st.pyplot(fig_eq_code)
        # 4. Set_No Plot
        with col2:
            st.subheader("4. Set Number By Hour")
            set_no_counts = filtered_data['set_no'].value_counts()
            fig_set_no = plt.figure(figsize=(8, 6))
            plt.pie(set_no_counts, labels=set_no_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Pastel1", len(set_no_counts)))
            plt.title("Set Number Distribution")
            st.pyplot(fig_set_no)
        # Empty space for better alignment between the two rows
        st.empty()
        # 5. Arrival Delays Plot
        with col1:
            st.subheader("5. Arrival Delay By Hour")
            filtered_data['status'] = filtered_data['arr_delay'].apply(lambda x: 'early' if x <= 0 else 'delayed')
            fig_dep_delay = plt.figure(figsize=(10, 6))
            sns.scatterplot(data=filtered_data, x='hr', y='arr_delay', hue='status', palette={'early': 'green', 'delayed': 'red'})
            plt.axhline(0, color='black', linestyle='--', label="Baseline (on-time)")
            plt.title("Arr Delay vs Hour")
            plt.xlabel('Hour')
            plt.ylabel('Arrival Delay')
            plt.legend()
            st.pyplot(fig_dep_delay)
        # 6. Group, Assistance, Duty vs hr
        with col2:
            st.subheader("6. Group, Assistance, Duty Counts By Hour")
            df_group = filtered_data.groupby('hr')[['group', 'assistance', 'duty']].sum().reset_index()
            fig_group_assistance_duty = plt.figure(figsize=(10, 6))
            sns.lineplot(data=df_group, x='hr', y='group', label='Group', color='blue', marker='*', linewidth=2)
            sns.lineplot(data=df_group, x='hr', y='assistance', label='Assistance', color='orange', marker='^', linewidth=2)
            sns.lineplot(data=df_group, x='hr', y='duty', label='Duty', color='green', marker='v', linewidth=2)
            plt.title("Count of Group, Assistance, Duty vs Hour")
            plt.xlabel('Hour')
            plt.ylabel('Count')
            plt.legend()
            st.pyplot(fig_group_assistance_duty)
        # Empty space for better alignment between rows
        st.empty()
        # 7. Premier, Plus, Standard, Wheelchair, Wheelchair Companion vs hr
        with col1:
            st.subheader("7. Premier, Plus, Standard, Wheelchair, Wheelchair Companion Counts By Hour")
            df_wheelchair = filtered_data.groupby('hr')[['premier', 'plus', 'standard', 'wheelchair', 'wheelchair_companion']].sum().reset_index()
            fig_wheelchair = plt.figure(figsize=(10, 6))
            sns.lineplot(data=df_wheelchair, x='hr', y='premier', label='Premier', color='purple', marker='*', linewidth=2)
            sns.lineplot(data=df_wheelchair, x='hr', y='plus', label='Plus', color='red', marker='^', linewidth=2)
            sns.lineplot(data=df_wheelchair, x='hr', y='standard', label='Standard', color='blue', marker='v', linewidth=2)
            sns.lineplot(data=df_wheelchair, x='hr', y='wheelchair', label='Wheelchair', color='green', marker='o', linewidth=2)
            sns.lineplot(data=df_wheelchair, x='hr', y='wheelchair_companion', label='Wheelchair Companion', color='yellow', marker='|', linewidth=2)
            plt.title("Count of Premier, Plus, Standard, Wheelchair, Wheelchair Companion vs Hour")
            plt.xlabel('Hour')
            plt.ylabel('Count')
            plt.legend()
            st.pyplot(fig_wheelchair)
        # 8. Senior, Adult, Youth, Child, Guide Dog vs hr
        with col2:
            st.subheader("8. Senior, Adult, Youth, Child, Guide Dog Counts By Hour")
            df_people = filtered_data.groupby('hr')[['senior', 'adult', 'youth', 'child', 'guide_dog']].sum().reset_index()
            fig_people = plt.figure(figsize=(10, 6))
            sns.lineplot(data=df_people, x='hr', y='senior', label='Senior', color='green', marker='*', linewidth=2)
            sns.lineplot(data=df_people, x='hr', y='adult', label='Adult', color='purple', marker='^', linewidth=2)
            sns.lineplot(data=df_people, x='hr', y='youth', label='Youth', color='cyan', marker='v', linewidth=2)
            sns.lineplot(data=df_people, x='hr', y='child', label='Child', color='orange', marker='o', linewidth=2)
            sns.lineplot(data=df_people, x='hr', y='guide_dog', label='Guide Dog', color='pink', marker='|', linewidth=2)
            plt.title("Count of Senior, Adult, Youth, Child, Guide Dog vs Hour")
            plt.xlabel('Hour')
            plt.ylabel('Count')
            plt.legend()
            st.pyplot(fig_people)
        # Empty space for better alignment between rows
        st.empty()
        # Create the map with the filtered data
        # Initialize session state to store colors and varied coordinates
        if "marker_data" not in st.session_state:
            st.session_state["marker_data"] = []
        # Check if DataFrame has changed
        df_hash = dataframe_hash(filtered_data)  # Get the hash of the current DataFrame
        # Ensure that the DataFrame columns are converted to native Python types
        df_filtered_data = filtered_data.applymap(lambda x: x.item() if hasattr(x, "item") else x)
        # Only update if the DataFrame has changed
        if "df_hash" not in st.session_state or st.session_state["df_hash"] != df_hash:
            # Store the hash to track changes
            st.session_state["df_hash"] = df_hash
            # Rebuild the marker data if the DataFrame has changed
            st.session_state["marker_data"] = []
            for _, row in df_filtered_data.iterrows():
                # Add variation to coordinates
                varied_lat, varied_lon = add_variation(row["latitude"], row["longitude"])
                # Generate random color
                color = random_color()
                # Append marker data to session state
                st.session_state["marker_data"].append({
                    "lat": float(varied_lat),
                    "lon": float(varied_lon),
                    "color": f"rgba({color[0]}, {color[1]}, {color[2]}, {color[3] / 255:.2f})",
                    "popup": (
                            f"<b>Train:</b> {row['train_no']}<br>"
                            f"<b>Date:</b> {row['scheduled_dt']}<br>"
                            f"<b>Hour:</b> {row['hr']}<br>"
                            f"<b>Route:</b> {row['route']}<br>"
                            f"<b>Carrier:</b> {row['carrier']}<br>"
                            f"<b>Equipment:</b> {row['eq_code']}<br>"
                            f"<b>Set:</b> {row['set_no']}<br>"
                            f"<b>Station:</b> {row['station']}<br>"
                            f"<b>Country:</b> {row['country']}<br>"
                            f"<b>DepartureDelay:</b> {row['dep_delay']}<br>"
                            f"<b>ArrivalDelay:</b> {row['arr_delay']}<br>"
                            f"<b>Group:</b> {row['group']}<br>"
                            f"<b>Assistance:</b> {row['assistance']}<br>"
                            f"<b>Duty:</b> {row['duty']}<br>"
                            f"<b>Premier:</b> {row['premier']}<br>"
                            f"<b>Plus:</b> {row['plus']}<br>"
                            f"<b>Standard:</b> {row['standard']}<br>"
                            f"<b>Wheelchair:</b> {row['wheelchair']}<br>"
                            f"<b>WheelchairCompanion:</b> {row['wheelchair_companion']}<br>"
                            f"<b>Senior:</b> {row['senior']}<br>"
                            f"<b>Adult:</b> {row['adult']}<br>"
                            f"<b>Youth:</b> {row['youth']}<br>"
                            f"<b>Child:</b> {row['child']}<br>"
                            f"<b>GuideDog:</b> {row['guide_dog']}"
                        ),
                })
        # Create a map centered around the first coordinate in the DataFrame
        first_location = [df_filtered_data.iloc[0]["latitude"], df_filtered_data.iloc[0]["longitude"]]
        zoom_start = int(df_filtered_data.iloc[0]["zoom"])
        m = folium.Map(location=first_location, zoom_start=zoom_start, tiles="CartoDB Positron", attr="CartoDB Positron")
        # Add markers with preserved session state data
        for marker in st.session_state["marker_data"]:
            folium.CircleMarker(
                    location=[marker["lat"], marker["lon"]],
                    radius=5,
                    color=marker["color"],
                    fill=True,
                    fill_color=marker["color"],
                    fill_opacity=0.8,
                    popup=folium.Popup(marker["popup"], max_width=300),
                ).add_to(m)
        # Display map in Streamlit
        st.title("Train Information Map")
        st_folium(m, width=725)
        # Search Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif tab == "Passenger":
    st.markdown("<div class='subheader'>Passenger</div>", unsafe_allow_html=True)
    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    # Train search form
    with st.container():
        st.title("Passenger Data Visualization")
        # Load data
        df = load_train_data()
        df = df[['train_no','scheduled_dt','station','latitude','longitude','zoom','hr','00~02','03~12','13~19','20~29','30~39','40~49','50~59','60~69','70~79','80~89','90~99','100+','eu_count','noneu_count','passeneger_counts','child_meal','dairy_free_meal','diabetic_meal','gluten_free_meal','kosher_meal','low_fat_meal','low_salt_meal','halal_meal','vegan_meal','vegetarian_meal','standard_meal']]
        #Travel Date
        df['scheduled_dt'] = pd.to_datetime(df['scheduled_dt']).dt.date
        min_date = df['scheduled_dt'].min()
        max_date = df['scheduled_dt'].max()
        travel_date = st.date_input("Select Travel Date",
                                    min_value=min_date,
                                    max_value=max_date,
                                    key="travel_date")
        #Boarding Station
        boarding_station = df['station'].unique()
        # Create the dropdown
        selected_station = st.selectbox('Select A Boarding Station', boarding_station)
        # Range slider for selecting time range (5 AM to 10 PM)
        start_hour, end_hour = st.slider(
            "Select departure time range",
            min_value=5,  # No leading zero
            max_value=22,
            value=(5, 22),  # No leading zero
            step=1,
        )
        # Filter data based on selected time range
        filtered_data = df[((df['hr'] >= start_hour) & (df['hr'] < end_hour)) & (df['station'] == selected_station) & (df['scheduled_dt'] == travel_date)]
        filtered_data.replace('-', None, inplace=True)
        # Replace None or NaN values with 0
        filtered_data = filtered_data.fillna(0)
        st.write(filtered_data)
        # Title of the Dashboard
        st.title("Pax Data Dashboard")

        # 1. EU/NonEu Plot
        st.subheader("1. Pax By Nationality")
        agg_data = filtered_data.groupby('hr').agg({
            'eu_count': 'sum',
            'noneu_count': 'sum'
            }).reset_index()
        # Prepare data for the donut plot
        donut_data = agg_data[['eu_count', 'noneu_count']].sum().reset_index()
        donut_data.columns = ['category', 'count']
        # Create a donut plot
        fig = px.pie(
            donut_data,
            names='category',
            values='count',
            title='Distribution of EU vs Non-EU Count',
            hole=0.4  # This makes it a donut chart
            )
        # Display the plot in Streamlit
        st.plotly_chart(fig)
        # Empty space for better alignment between rows
        st.empty()

        # 2. Meal Plot
        st.subheader("2. Meal By Hour")
        agg_data = filtered_data.groupby('hr').agg({
                'passeneger_counts': 'sum',
                'child_meal': 'sum',
                'dairy_free_meal': 'sum',
                'diabetic_meal': 'sum',
                'gluten_free_meal': 'sum',
                'kosher_meal': 'sum',
                'low_fat_meal': 'sum',
                'low_salt_meal': 'sum',
                'halal_meal': 'sum',
                'vegan_meal': 'sum',
                'vegetarian_meal': 'sum',
                'standard_meal': 'sum'
            }).reset_index()
        # Melt the DataFrame for stacked bar chart
        stacked_data = agg_data.melt(
            id_vars=['hr', 'passeneger_counts'],
            value_vars=[
                    'child_meal', 'dairy_free_meal', 'diabetic_meal', 'gluten_free_meal',
                    'kosher_meal', 'low_fat_meal', 'low_salt_meal', 'halal_meal',
                    'vegan_meal', 'vegetarian_meal', 'standard_meal'
                ],
            var_name='meal_type',
            value_name='meal_count'
            )
        # Create the stacked bar chart
        fig = px.bar(
                stacked_data,
                x='hr',
                y='meal_count',
                color='meal_type',
                title='Passenger Counts with Meal Distribution',
                labels={'hr': 'Hour', 'meal_count': 'Meal Count'},
                text_auto=True
                )
        # Add total passenger count as line on top
        fig.add_scatter(
                x=agg_data['hr'],
                y=agg_data['passeneger_counts'],
                mode='lines+markers',
                name='Total Passengers',
                line=dict(color='black', width=2, dash='dash')
                )
        # Display the plot in Streamlit
        st.plotly_chart(fig)
        # Empty space for better alignment between rows
        st.empty()

        # 2. Pax Age Plot
        st.subheader("3. Pax Age Group By Hour")
        agg_data = filtered_data.groupby('hr').agg({
                '00~02': 'sum',
                '03~12': 'sum',
                '13~19': 'sum',
                '20~29': 'sum',
                '30~39': 'sum',
                '40~49': 'sum',
                '50~59': 'sum',
                '60~69': 'sum',
                '70~79': 'sum',
                '80~89': 'sum',
                '90~99': 'sum',
                '100+': 'sum'
            }).reset_index()
        # Melt the DataFrame for bar chart
        bar_data = agg_data.melt(
            id_vars=['hr'],
            value_vars=[
                '00~02', '03~12', '13~19', '20~29', '30~39', '40~49', 
                '50~59', '60~69', '70~79', '80~89', '90~99', '100+'
            ],
            var_name='range',
            value_name='count'
        )
        # Create the bar chart
        fig = px.bar(
            bar_data,
            x='hr',
            y='count',
            color='range',
            barmode='group',
            title='Pax Age Group By Hour',
            labels={'hr': 'Hour', 'count': 'Count', 'range': 'Range'}
        )
        # Display the chart in Streamlit
        st.plotly_chart(fig)

        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
elif tab == "Hotel":
    st.markdown("<div class='subheader'>Hotels</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='tab-content'>
            <h3 class='intro-title'>Find Your Hotel</h3>
            <p class='intro-text'>Search for hotels for a destination with check-in dates</p>
        </div>
    """, unsafe_allow_html=True)
    # Add extra space
    st.markdown('<div class="extra-space"></div>', unsafe_allow_html=True)
    # Hotel search form
    # Load data
    df = load_train_data()
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
             #Boarding Station
            boarding_station = df['station'].unique()
            # Create the dropdown
            destination = st.selectbox('Select A Boarding Station', boarding_station)
        with col2:
            df['scheduled_dt'] = pd.to_datetime(df['scheduled_dt']).dt.date
            min_date = df['scheduled_dt'].min()
            max_date = df['scheduled_dt'].max()
            checkin_date = st.date_input("Select Travel Date",
                                         min_value=min_date,
                                         max_value=max_date,
                                         key="checkin_date")
        # Search Button
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        if st.button("Search Hotels", key="hotel_button", use_container_width=True):
            st.write(f"Searching for hotels in {destination} for {checkin_date}.....")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Dummy bot responses
    responses = {
        "hello": "Hi there! How can I assist you today?",
        "how are you": "I'm just a bot, but I'm here to help!",
        "help": "Sure! Let me know what you need help with.",
        "bye": "Goodbye! Have a great day!",
    }

    # Default response for unknown inputs
    default_response = "I'm not sure how to respond to that. Can you rephrase?"

    # Initialize session state to store conversation history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Chat interface
    st.title("Dummy Bot")

    # Display chat history
    for message in st.session_state["messages"]:
        st.markdown(f"**{message['user']}:** {message['text']}")

    # Input form for user message
    with st.form(key="chat_form", clear_on_submit=True):  # Clear input after submission
        user_input = st.text_input("You:", key="user_input", placeholder="Type your message here...")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        # Save user input to chat history
        st.session_state["messages"].append({"user": "You", "text": user_input})

        # Generate bot response
        response = responses.get(user_input.lower(), default_response)
        st.session_state["messages"].append({"user": "Bot", "text": response})
