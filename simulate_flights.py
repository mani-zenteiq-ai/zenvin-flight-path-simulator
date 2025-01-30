import numpy as np
import pandas as pd
import os
import argparse
import folium
from folium.plugins import AntPath

# Constants for GPS conversion
EARTH_RADIUS = 6371000  # Earth's radius in meters
METERS_PER_DEGREE_LAT = 111000  # Meters per degree of latitude

# Function to convert GPS to Cartesian
def gps_to_cartesian(lat, lon, alt, ref_lat, ref_lon, ref_alt):
    """
    Convert GPS coordinates to Cartesian coordinates.

    Parameters
    ----------
    lat : float
        Latitude in degrees
    lon : float
        Longitude in degrees
    alt : float
        Altitude in meters
    ref_lat : float
        Reference latitude in degrees
    ref_lon : float
        Reference longitude in degrees
    ref_alt : float
        Reference altitude in meters

    Returns
    -------
    x, y, z : numpy array
        Cartesian coordinates in meters
    """
    x = (lon - ref_lon) * np.cos(np.radians(ref_lat)) * METERS_PER_DEGREE_LAT
    y = (lat - ref_lat) * METERS_PER_DEGREE_LAT
    z = alt - ref_alt
    return np.array([x, y, z])

# Function to convert Cartesian to GPS
def cartesian_to_gps(x, y, z, ref_lat, ref_lon, ref_alt):
    """
    Convert Cartesian coordinates to GPS coordinates.

    Parameters
    ----------
    x : float
        X coordinate in meters
    y : float
        Y coordinate in meters
    z : float
        Z coordinate in meters
    ref_lat : float
        Reference latitude in degrees
    ref_lon : float
        Reference longitude in degrees
    ref_alt : float
        Reference altitude in meters

    Returns
    -------
    lat : float
        Latitude in degrees
    lon : float
        Longitude in degrees
    alt : float
        Altitude in meters
    """
    lat = ref_lat + (y / METERS_PER_DEGREE_LAT)
    lon = ref_lon + (x / (METERS_PER_DEGREE_LAT * np.cos(np.radians(ref_lat))))
    alt = ref_alt + z
    return lat, lon, alt

def simulate_flights(flight_file="flights_gps.csv", num_steps=100):
    # Load flight details from CSV
    """
    Simulate GPS flight paths and save them to a Folium map.

    Parameters
    ----------
    flight_file : str
        Path to a CSV file containing flight details:
            - Flight_ID (int): Unique identifier for the flight
            - Start_Latitude (float): Latitude of the starting point
            - Start_Longitude (float): Longitude of the starting point
            - Start_Altitude (float): Altitude of the starting point
            - End_Latitude (float): Latitude of the ending point
            - End_Longitude (float): Longitude of the ending point
            - End_Altitude (float): Altitude of the ending point
            - Velocity (float): Speed of the flight in meters per second
    num_steps : int
        Number of time steps for the simulation

    Notes
    -----
    The function will create a directory named "flight_positions_by_time" and save
    each timestamp's data to a separate CSV file. The CSV files will have the same
    structure as the input CSV file, with additional columns for Latitude, Longitude,
    and Altitude at each timestamp.

    The function will also generate a 3D plot of all flights, with start and end markers
    and direction arrows.
    """
    flights_df = pd.read_csv(flight_file)

    # Time step for simulation
    TIME_STEP = 0.5  # Default time step (seconds)

    # Create output directory for flight position data
    output_dir = "flight_positions_by_time"
    os.makedirs(output_dir, exist_ok=True)

    # Reference GPS location (use first flight's start point)
    ref_lat = flights_df.iloc[0]["Start_Latitude"]
    ref_lon = flights_df.iloc[0]["Start_Longitude"]
    ref_alt = flights_df.iloc[0]["Start_Altitude"]

    # Initialize map centered around India
    flight_map = folium.Map(location=[ref_lat, ref_lon], zoom_start=5)

    # Data storage for timestep outputs
    time_steps_data = {}

    # Process each flight
    for _, flight in flights_df.iterrows():
        flight_id = flight["Flight_ID"]

        # Convert GPS start and end to Cartesian
        start_point = gps_to_cartesian(flight["Start_Latitude"], flight["Start_Longitude"], flight["Start_Altitude"], ref_lat, ref_lon, ref_alt)
        end_point = gps_to_cartesian(flight["End_Latitude"], flight["End_Longitude"], flight["End_Altitude"], ref_lat, ref_lon, ref_alt)
        velocity = flight["Velocity"]

        # Compute displacement and direction
        displacement = end_point - start_point
        distance_total = np.linalg.norm(displacement)
        unit_direction = displacement / distance_total

        # Generate time steps for this flight
        time_total = distance_total / velocity
        time_steps = np.linspace(0, time_total, num_steps)

        # Compute positions at each time step
        flight_path = []
        for t in time_steps:
            position = start_point + velocity * t * unit_direction
            lat, lon, alt = cartesian_to_gps(position[0], position[1], position[2], ref_lat, ref_lon, ref_alt)
            flight_path.append((lat, lon))

            # Store timestep data
            if t not in time_steps_data:
                time_steps_data[t] = []
            time_steps_data[t].append([flight_id, lat, lon, alt])

        # Add flight path to map
        folium.PolyLine(flight_path, color="blue", weight=2.5, opacity=0.8, tooltip=f"Flight {flight_id}").add_to(flight_map)

        # Add animated AntPath for visual effect
        AntPath(locations=flight_path, color="blue", delay=1000).add_to(flight_map)

        # Add start and end markers
        folium.Marker(
            location=flight_path[0], 
            icon=folium.Icon(color="green", icon="plane", prefix="fa"),
            popup=f"Start of Flight {flight_id}"
        ).add_to(flight_map)

        folium.Marker(
            location=flight_path[-1], 
            icon=folium.Icon(color="red", icon="flag", prefix="fa"),
            popup=f"End of Flight {flight_id}"
        ).add_to(flight_map)

    # Save flight position data by timestamp
    for t, data in time_steps_data.items():
        df_time = pd.DataFrame(data, columns=["Flight_ID", "Latitude", "Longitude", "Altitude"])
        timestamp_filename = f"{output_dir}/flight_positions_t{t:.1f}.csv"
        df_time.to_csv(timestamp_filename, index=False)

    # Save map to HTML file
    flight_map.save("flights_map.html")
    print("Flight paths visualized and saved as 'flights_map.html'")
    print(f"Flight data saved per timestep in '{output_dir}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate multiple flights based on GPS data and visualize on a map.")
    parser.add_argument("--file", type=str, default="flights_gps.csv", help="Path to the flight data CSV file (default: flights_gps.csv)")
    parser.add_argument("--num_steps", type=int, default=100, help="Number of timesteps for simulation (default: 100)")

    args = parser.parse_args()

    simulate_flights(args.file, args.num_steps)
