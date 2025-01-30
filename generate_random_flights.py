import numpy as np
import pandas as pd
import argparse

# Define India's latitude and longitude range
INDIA_LAT_RANGE = (8.0, 37.0)  # Approximate latitudes of India
INDIA_LON_RANGE = (68.0, 97.0)  # Approximate longitudes of India
ALTITUDE_RANGE = (100, 12000)  # Altitude in meters (100m to 12,000m)
VELOCITY_RANGE = (200, 900)  # Flight velocity in km/h (200-900 km/h)

def generate_random_flights(num_flights, output_file="flights_gps.csv"):
    # Generate random flight data
    """
    Generate a specified number of random flights within India's geographic range.

    Parameters
    ----------
    num_flights : int
        The number of random flights to generate.
    output_file : str, optional
        The file path to save the generated flight data to (default: "flights_gps.csv").

    Returns
    -------
    None
    """
    flight_data = []
    for flight_id in range(1, num_flights + 1):
        start_lat = np.random.uniform(*INDIA_LAT_RANGE)
        start_lon = np.random.uniform(*INDIA_LON_RANGE)
        start_alt = np.random.uniform(*ALTITUDE_RANGE)

        end_lat = np.random.uniform(*INDIA_LAT_RANGE)
        end_lon = np.random.uniform(*INDIA_LON_RANGE)
        end_alt = np.random.uniform(*ALTITUDE_RANGE)

        velocity = np.random.uniform(*VELOCITY_RANGE)  # Random velocity in km/h

        flight_data.append([flight_id, start_lat, start_lon, start_alt, end_lat, end_lon, end_alt, velocity])

    # Create a DataFrame
    df_flights = pd.DataFrame(flight_data, columns=[
        "Flight_ID", "Start_Latitude", "Start_Longitude", "Start_Altitude",
        "End_Latitude", "End_Longitude", "End_Altitude", "Velocity"
    ])

    # Save to CSV
    df_flights.to_csv(output_file, index=False)
    print(f"Generated {num_flights} random flights and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random flight data within India.")
    parser.add_argument("--num_flights", type=int, default=10, help="Number of flights to generate")
    parser.add_argument("--output", type=str, default="flights_gps.csv", help="Output CSV file name (default: flights_gps.csv)")

    args = parser.parse_args()

    generate_random_flights(args.num_flights, args.output)
