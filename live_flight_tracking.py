import requests
import folium
from flask import Flask, render_template, jsonify

# Define India's center coordinates
INDIA_CENTER = [20.5937, 78.9629]  
ADSB_API_URL = "https://adsbexchange.com/api/v2/lat=20.5937/lon=78.9629/dist=100"

# Initialize Flask app
app = Flask(__name__)

def fetch_realtime_flights():
    """Fetch real-time flights from ADS-B Exchange API."""
    try:
        response = requests.get(ADSB_API_URL)
        response.raise_for_status()
        data = response.json()

        filtered_flights = []
        for flight in data.get("ac", []):
            if "lat" in flight and "lon" in flight:  # Ensure lat/lon exist
                filtered_flights.append({
                    "Flight_ID": flight.get("hex", "Unknown"),
                    "Latitude": flight["lat"],
                    "Longitude": flight["lon"],
                    "Altitude": flight.get("alt_baro", "N/A"),
                    "Velocity": flight.get("gs", "N/A"),
                    "Heading": flight.get("track", "N/A"),
                    "Origin_Country": flight.get("r", "N/A"),
                    "Vertical_Rate": flight.get("baro_rate", "N/A")
                })
        return filtered_flights
    except requests.RequestException as e:
        print(f"❌ Error fetching data from ADS-B Exchange: {e}")
        return []

def generate_base_map():
    """Generate and save a static base map for India."""
    flight_map = folium.Map(location=INDIA_CENTER, zoom_start=5)
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