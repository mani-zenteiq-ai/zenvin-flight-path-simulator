
# **Flight Path Simulation and Visualization**

This repository contains Python scripts to **generate random flight data** within India and **visualize flight paths** on an interactive folium map. The project consists of two main scripts:

1. **`generate_random_flights.py`** - Generates random flight data and saves it as a CSV file.
2. **`simulate_flights.py`** - Reads flight data, simulates movement, saves timestamped flight data, and overlays paths on a folium-based map.

---

## **Installation**
Before running the scripts, install the required dependencies:
```bash

uv init
uv add ruff
uv pip install numpy pandas folium argparse
```

---

## **1️⃣ Generating Random Flight Data**
### **Script: `generate_random_flights.py`**
This script generates random flight data within India's geographical bounds and saves it as a CSV file.

### **Usage**
```bash
uv run python generate_random_flights.py --num_flights <NUMBER> --output <FILENAME>
```

### **Arguments**
| Argument       | Type  | Default             | Description |
|---------------|-------|---------------------|-------------|
| `--num_flights` | `int`  | **Required** | Number of flights to generate |
| `--output` | `str`  | `flights_gps.csv` | Output CSV file name |

### **Example**
```bash
uv run python generate_random_flights.py --num_flights 100 --output flights_gps.csv
```
- Generates **100 flights** and saves them to `flights_gps.csv`.

### **Example CSV Output (`flights_gps.csv`)**
```
Flight_ID,Start_Latitude,Start_Longitude,Start_Altitude,End_Latitude,End_Longitude,End_Altitude,Velocity
1,22.4563,75.8745,3500,30.4561,78.9563,10000,750
2,15.8745,81.4523,200,28.1456,74.5689,9000,580
3,10.2145,76.8745,2500,26.7895,85.1245,11000,660
```

---

## **2️⃣ Simulating and Visualizing Flights**
### **Script: `simulate_flights.py`**
This script reads flight data from a CSV file, simulates movement, saves flight position data at **each timestep**, and overlays the flight paths on an **interactive folium map**.

### **Usage**
```bash
uv run python simulate_flights.py --file <CSV_FILE> --num_steps <NUMBER>
```

### **Arguments**
| Argument       | Type  | Default             | Description |
|---------------|-------|---------------------|-------------|
| `--file`      | `str`  | `flights_gps.csv` | Input CSV file with flight data |
| `--num_steps` | `int`  | `100` | Number of timesteps for simulation |

### **Example**
```bash
uv python simulate_flights.py --file flights_gps.csv --num_steps 50
```
- Reads **`flights_gps.csv`**, simulates **50 timesteps**, saves **timestamped flight data**, and generates an **interactive map**.

---

## **3️⃣ Output Files**
### **1. Timestamped Flight Data (`flight_positions_by_time/`)**
This script generates one CSV file per timestep, containing all flights' positions at that moment.

#### **Example:**
```
flight_positions_by_time/flight_positions_t0.0.csv
flight_positions_by_time/flight_positions_t0.5.csv
flight_positions_by_time/flight_positions_t1.0.csv
...
```
Each file contains **the GPS position of every flight and veclocity at that specific timestamp**.

#### **Example CSV (`flight_positions_t0.0.csv`)**
```
Flight_ID,Latitude,Longitude,Altitude,Velocity
1,22.4563,75.8745,3500,750
2,15.8745,81.4523,200,580
```

---

### **2. Interactive Flight Map (`flights_map.html`)**
- Displays **flight paths as blue lines**  
- Uses **green airplane icons for start points**  
- Uses **red flag icons for end points**  
- Flight paths are **animated** using `AntPath`  
- Fully **interactive map with zoom and pan**  

To view the interactive flight map, simply open **`flights_map.html`** in any web browser.

The folloing is an example of the map. 

![alt text](flight_paths.png)

---

## **Project Overview**
| Script | Purpose |
|--------|---------|
| `generate_random_flights.py` | Generates random flight data within India |
| `simulate_flights.py` | Simulates and visualizes flights on an interactive folium map and saves timestamped flight data |

---

## **📌 Notes**
- The **flight paths are random** and do not represent real-world flights.
- The **map is saved as `flights_map.html`** and can be opened in any web browser.
- The **flight position data is saved per timestamp** in `flight_positions_by_time/`.

---

## **📜 License**
This project is open-source and free to use.

---
