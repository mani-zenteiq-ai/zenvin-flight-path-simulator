Here is the **`README.md`** file for your GitHub repository, documenting both `generate_random_flights.py` and `simulate_flights_gps_folium.py`.  

---

# **Flight Path Simulation and Visualization**

This repository contains Python scripts to **generate random flight data** within India and **visualize flight paths** on an interactive map using `folium`. The project consists of two main scripts:

1. **`generate_random_flights.py`** - Generates random flight data and saves it as a CSV file.
2. **`simulate_flights.py`** - Reads flight data, simulates movement, and overlays paths on a folium-based map. Generates flight data as multiple .csv files based on timestamp.

---

## **Installation**
Before running the scripts, install the required dependencies:
```bash
pip install numpy pandas folium argparse
```

---

## **1️⃣ Generating Random Flight Data**
### **Script: `generate_random_flights.py`**
This script generates random flight data within India's geographical bounds and saves it as a CSV file.

### **Usage**
```bash
python generate_random_flights.py --num_flights <NUMBER> --output <FILENAME>
```

### **Arguments**
| Argument       | Type  | Default             | Description |
|---------------|-------|---------------------|-------------|
| `--num_flights` | `int`  | **Required** | Number of flights to generate |
| `--output` | `str`  | `flights_gps.csv` | Output CSV file name |

### **Example**
```bash
python generate_random_flights.py --num_flights 100 --output my_flights.csv
```
- Generates **100 flights** and saves them to `my_flights.csv`.

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
This script reads flight data from a CSV file, simulates movement, and overlays the flight paths on an **interactive folium map**.

### **Usage**
```bash
python simulate_flights.py --file <CSV_FILE> --num_steps <NUMBER>
```

### **Arguments**
| Argument       | Type  | Default             | Description |
|---------------|-------|---------------------|-------------|
| `--file`      | `str`  | `flights_gps.csv` | Input CSV file with flight data |
| `--num_steps` | `int`  | `100` | Number of timesteps for simulation |

### **Example**
```bash
python simulate_flights.py --file flights_gps.csv --num_steps 50
```
- Reads **`flights_gps.csv`**, simulates **50 timesteps**, and generates an **interactive map**.

### **Output: `flights_map.html`**
- An **interactive map** with:
  - **Blue flight paths** over India
  - **Green airplane markers** for start points
  - **Red flag markers** for end points
  - **Animated flight movements** using `AntPath`

### **Example Map Screenshot**
![Flight Map Preview](https://upload.wikimedia.org/wikipedia/commons/8/83/India_location_map.svg)  
(*Replace with actual screenshot of your generated `flights_map.html`.*)

---

## **Project Overview**
| Script | Purpose |
|--------|---------|
| `generate_random_flights.py` | Generates random flight data within India |
| `simulate_flights.py` | Simulates and visualizes flights on an interactive folium map |

---

## **📌 Notes**
- The **flight paths are random** and do not represent real-world flights.
- The **map is saved as `flights_map.html`** and can be opened in any web browser.
- You can modify the **number of timesteps** for more detailed simulations.

---

## **📜 License**
This project is open-source and free to use.

---

Now your repository has a complete **README.md** with installation instructions, usage examples, and expected outputs. 🚀 Let me know if you need further modifications!
