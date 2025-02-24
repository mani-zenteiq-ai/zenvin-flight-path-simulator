import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster, AntPath

# Define India's latitude and longitude range
INDIA_LAT_RANGE = (8.0, 37.0)  # Approximate latitudes of India
INDIA_LON_RANGE = (68.0, 97.0)  # Approximate longitudes of India

# OpenSky API endpoint
OPENSKY_API_URL = "https://opensky-network.org/api/states/all"

def fetch_realtime_flights():
    """Fetch real-time flights from OpenSky API filtered to India."""
    try:
        response = requests.get(OPENSKY_API_URL)
        response.raise_for_status()  # Raise error for bad responses
        data = response.json()
        flights = data.get("states", [])

        filtered_flights = []
        for flight in flights:
            if flight[5] is not None and flight[6] is not None:  # Ensure lat/lon exist
                lat, lon = flight[6], flight[5]
                if INDIA_LAT_RANGE[0] <= lat <= INDIA_LAT_RANGE[1] and INDIA_LON_RANGE[0] <= lon <= INDIA_LON_RANGE[1]:
                    filtered_flights.append({
                        "Flight_ID": flight[0],
                        "Latitude": lat,
                        "Longitude": lon,
                        "Altitude": flight[7],
                        "Velocity": flight[9],
                        "Heading": flight[10],
                        "Origin_Country": flight[13],
                        "Vertical_Rate": flight[17]
                    })
        return filtered_flights
    except requests.RequestException as e:
        print(f"❌ Error fetching data from OpenSky API: {e}")
        return []

def load_simulated_flights(file="flights_gps.csv"):
    """Load simulated flights from a CSV file."""
    try:
        df = pd.read_csv(file)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"❌ Error loading simulated flight data: {e}")
        return []

def visualize_flights(realtime_flights, simulated_flights):
    """Visualize real-time and simulated flights on a folium map."""
    # Center map on India
    india_center = [20.5937, 78.9629]
    flight_map = folium.Map(location=india_center, zoom_start=5)

    # Use MarkerCluster for better visualization
    realtime_cluster = MarkerCluster(name="Real-Time Flights").add_to(flight_map)
    simulated_cluster = MarkerCluster(name="Simulated Flights").add_to(flight_map)

    # Plot real-time flights
    for flight in realtime_flights:
        popup_text = f"""
        <b>Flight ID:</b> {flight['Flight_ID']}<br>
        <b>Origin:</b> {flight['Origin_Country']}<br>
        <b>Altitude:</b> {flight['Altitude']} m<br>
        <b>Velocity:</b> {flight['Velocity']} m/s<br>
        <b>Heading:</b> {flight['Heading']}°<br>
        <b>Vertical Rate:</b> {flight['Vertical_Rate']} m/s
        """
        
        folium.Marker(
            location=[flight['Latitude'], flight['Longitude']],
            popup=popup_text,
            icon=folium.Icon(color="red", icon="plane", prefix="fa")
        ).add_to(realtime_cluster)

        # Add AntPath showing flight direction
        AntPath(
            locations=[
                [flight['Latitude'], flight['Longitude']],
                [flight['Latitude'] + 0.1 * (flight['Velocity'] / 250),  
                 flight['Longitude'] + 0.1 * (flight['Velocity'] / 250)]
            ],
            color="red",
            weight=2
        ).add_to(flight_map)

    # Plot simulated flights
    for flight in simulated_flights:
        popup_text = f"""
        <b>Flight ID:</b> {flight['Flight_ID']}<br>
        <b>Start:</b> ({flight['Start_Latitude']}, {flight['Start_Longitude']})<br>
        <b>End:</b> ({flight['End_Latitude']}, {flight['End_Longitude']})<br>
        <b>Altitude:</b> {flight['Start_Altitude']} m to {flight['End_Altitude']} m<br>
        <b>Velocity:</b> {flight['Velocity']} km/h
        """

        folium.Marker(
            location=[flight['Start_Latitude'], flight['Start_Longitude']],
            popup=popup_text,
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")
        ).add_to(simulated_cluster)

        # Add simulated flight path
        folium.PolyLine(
            locations=[[flight['Start_Latitude'], flight['Start_Longitude']], 
                       [flight['End_Latitude'], flight['End_Longitude']]],
            color="blue",
            weight=2.5,
            opacity=0.8
        ).add_to(flight_map)

    # Add layer control
    folium.LayerControl().add_to(flight_map)

    # Save map
    flight_map.save("integrated_flight_map.html")
    print("✅ Integrated flight map saved as 'integrated_flight_map.html'")

# Fetch real-time flights over India
realtime_data = fetch_realtime_flights()

# Load simulated flight data
simulated_data = load_simulated_flights()

# Visualize both real-time and simulated flights on a map
if realtime_data or simulated_data:
    visualize_flights(realtime_data, simulated_data)
else:
    print("⚠️ No flights available for visualization.")