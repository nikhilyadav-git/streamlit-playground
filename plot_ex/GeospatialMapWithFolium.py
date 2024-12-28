import streamlit as st
import pandas as pd
import folium
import random
from streamlit_folium import st_folium

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

# Sample DataFrame
data = {
    "train_no": [9054, 9080],
    "scheduled_dt": ["27/12/2024", "27/12/2024"],
    "route": ["GBSPX-FRPNO", "GBSPX-FRPNO"],
    "carrier": ["Eurostar", "Eurostar"],
    "eq_code": ["E320", "E320"],
    "set_no": ["4024-4023", "4024-4023"],
    "station": ["London St Pancras Int'l", "London St Pancras Int'l"],
    "country": ["United Kingdom", "United Kingdom"],
    "latitude": [51.531427, 51.531427],
    "longitude": [-0.126133, -0.126133],
    "zoom": [17, 17],
    "dep_delay": ["", ""],
    "arr_delay": ["", ""],
}
df = pd.DataFrame(data)

# Ensure that the DataFrame columns are converted to native Python types
df = df.applymap(lambda x: x.item() if hasattr(x, "item") else x)

# Initialize session state to store colors and varied coordinates
if "marker_data" not in st.session_state:
    st.session_state["marker_data"] = []
    for _, row in df.iterrows():
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
                f"<b>Train Number:</b> {row['train_no']}<br>"
                f"<b>Scheduled Date:</b> {row['scheduled_dt']}<br>"
                f"<b>Route:</b> {row['route']}<br>"
                f"<b>Carrier:</b> {row['carrier']}<br>"
                f"<b>Eq Code:</b> {row['eq_code']}<br>"
                f"<b>Set No:</b> {row['set_no']}<br>"
                f"<b>Station:</b> {row['station']}<br>"
                f"<b>Country:</b> {row['country']}"
            ),
        })

# Create a map centered around the first coordinate in the DataFrame
first_location = [df.iloc[0]["latitude"], df.iloc[0]["longitude"]]
zoom_start = int(df.iloc[0]["zoom"])
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
