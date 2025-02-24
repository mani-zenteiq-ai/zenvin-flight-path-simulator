import requests
import folium
from folium.plugins import MarkerCluster, AntPath
import time
from flask import Flask, render_template_string

# Define India's latitude and longitude range
INDIA_LAT_RANGE = (8.0, 37.0)  # Approximate latitudes of India
INDIA_LON_RANGE = (68.0, 97.0)  # Approximate longitudes of India

# OpenSky API endpoint
OPENSKY_API_URL = "https://opensky-network.org/api/states/all"

# Initialize Flask app
app = Flask(__name__)

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
                        "Origin_Country": flight[2],
                        "Vertical_Rate": flight[11]
                    })
        return filtered_flights
    except requests.RequestException as e:
        print(f"❌ Error fetching data from OpenSky API: {e}")
        return []

def generate_mapo():
    """Generate an updated folium map with real-time flight data."""
    flights = fetch_realtime_flights()
    print (f'Number of flights: {len(flights)}')

    # Center map on India
    india_center = [20.5937, 78.9629]
    flight_map = folium.Map(location=india_center, zoom_start=5)

    # Use MarkerCluster for better visualization
    marker_cluster = MarkerCluster().add_to(flight_map)

    for flight in flights:
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
        ).add_to(marker_cluster)

        # Add an animated AntPath showing flight movement direction
        AntPath(
            locations=[
                [flight['Latitude'], flight['Longitude']],
                [flight['Latitude'] + 0.1 * (flight['Velocity'] / 250),  
                 flight['Longitude'] + 0.1 * (flight['Velocity'] / 250)]
            ],
            color="blue",
            weight=2
        ).add_to(flight_map)

    # Save the map as an HTML file
    flight_map.save("templates/realtime_flight_map.html")

def generate_map():
    """Generate an updated folium map with real-time flight data."""
    flights = fetch_realtime_flights()

    # Center map on India
    india_center = [20.5937, 78.9629]
    flight_map = folium.Map(location=india_center, zoom_start=5)

    # Use MarkerCluster for better visualization
    marker_cluster = MarkerCluster().add_to(flight_map)

    for flight in flights:
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
        ).add_to(marker_cluster)

        # Add an animated AntPath showing flight movement direction
        AntPath(
            locations=[
                [flight['Latitude'], flight['Longitude']],
                [flight['Latitude'] + 0.1 * (flight['Velocity'] / 250),  
                 flight['Longitude'] + 0.1 * (flight['Velocity'] / 250)]
            ],
            color="blue",
            weight=2
        ).add_to(flight_map)

    # Ensure the "static" directory exists
    import os
    os.makedirs("static", exist_ok=True)  

    # Save the map inside the "static" directory
    flight_map.save("static/realtime_flight_map.html")

#@app.route("/")
def live_map1():
    """Render the live updating flight map."""
    print ("Generating map...")
    generate_map()
    return render_template_string("""
    <html>
    <head>
        <title>Live Flight Tracking</title>
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        <h3>Live Flight Tracking Over India</h3>
        <iframe src="{{ url_for('static', filename='realtime_flight_map.html') }}" width="100%" height="600px"></iframe>
    </body>
    </html>
    """)

@app.route("/")
def live_map():
    """Render the live updating flight map."""
    generate_map()
    return render_template_string("""
    <html>
    <head>
        <title>Live Flight Tracking</title>
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        <h3>Live Flight Tracking Over India</h3>
        <iframe src="/static/realtime_flight_map.html" width="100%" height="600px"></iframe>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)