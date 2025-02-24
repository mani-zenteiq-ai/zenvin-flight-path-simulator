import requests
import folium
import json
from flask import Flask, render_template, jsonify

# Define India's latitude and longitude range
INDIA_LAT_RANGE = (8.0, 37.0)  
INDIA_LON_RANGE = (68.0, 97.0)  

# OpenSky API endpoint
OPENSKY_API_URL = "https://opensky-network.org/api/states/all"

# Initialize Flask app
app = Flask(__name__)

def fetch_realtime_flights():
    """Fetch real-time flights from OpenSky API with authentication."""
    OPENSKY_USERNAME = "srnimani"
    OPENSKY_PASSWORD = "Bulldog9902!"

    try:
        response = requests.get(OPENSKY_API_URL, auth=(OPENSKY_USERNAME, OPENSKY_PASSWORD))
        response.raise_for_status()
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

def generate_base_map():
    """Generate and save a static base map for India."""
    india_center = [20.5937, 78.9629]
    flight_map = folium.Map(location=india_center, zoom_start=5)

    # Save the base map once
    flight_map.save("templates/base_map.html")

@app.route("/")
def index():
    """Render the base map with JavaScript for live updates."""
    return render_template("index.html")

@app.route("/api/flights")
def api_flights():
    """Return real-time flight data as JSON for JavaScript to update."""
    flights = fetch_realtime_flights()
    return jsonify(flights)

if __name__ == "__main__":
    generate_base_map()  # Generate base map once
    app.run(debug=True, host="0.0.0.0", port=5050)