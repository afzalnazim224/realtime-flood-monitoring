import requests
import pandas as pd
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Define the base URL for the API
base_url = "http://environment.data.gov.uk/flood-monitoring"

# Function to get the latest readings
def get_latest_readings():
    url = f"{base_url}/data/readings?latest&startdate=2024-05-01&enddate=2024-05-20"
    # url = f"{base_url}/data/readings?latest"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        print("Failed to retrieve data")
        return None

# Function to get flood warnings
def get_flood_warnings():
    url = f"{base_url}/id/floods"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        print("Failed to retrieve data")
        return None

# Function to get stations near specific coordinates
def get_stations_near_coordinates(lat, long, radius):
    url = f"{base_url}/id/stations?lat={lat}&long={long}&dist={radius}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        print("Failed to retrieve data")
        return None

# Function to get flood data for a specific ID
def get_flood_by_id(flood_id):
    url = f"{base_url}/id/floodAreas/{flood_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data for flood ID {flood_id}")
        return None

# Function to save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to fetch and display data
def main():
    while True:
        # Fetch the latest readings
        latest_readings = get_latest_readings()
        if latest_readings:
            save_to_csv(latest_readings, "data/latest_readings.csv")
            print("Latest Readings:")
            print(pd.DataFrame(latest_readings).head())
            
            # Visualize the latest readings (example: water level over time)
            df_latest_readings = pd.DataFrame(latest_readings)
            plt.plot(df_latest_readings['dateTime'], df_latest_readings['value'], marker='o')
            plt.xlabel('Date and Time')
            plt.ylabel('Water Level')
            plt.title('Latest Water Level Readings')
          # Format x-axis dates for better readability
            # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            # plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))  # Adjust the number of ticks as needed
            plt.tight_layout()
            plt.show()
            
        else:
            print("No latest readings available")

        # Fetch flood warnings
        flood_warnings = get_flood_warnings()
        if flood_warnings:
            save_to_csv(flood_warnings, "data/flood_warnings.csv")
            print("\nFlood Warnings:")
            print(pd.DataFrame(flood_warnings).head())
            
            # Visualize flood warnings (example: count of warnings per severity level)
            df_flood_warnings = pd.DataFrame(flood_warnings)
            plt.bar(df_flood_warnings['severity'], df_flood_warnings['severityLevel'])
            plt.xlabel('Severity Level')
            plt.ylabel('Count')
            plt.title('Flood Warnings by Severity Level')
            plt.tight_layout()
            plt.show()
            
            # Extract flood ID from the first warning
            first_flood_id_url = flood_warnings[0]['@id']
            flood_id = first_flood_id_url.split('/')[-1]  # Extract the ID from the URL
            print(f"\nExtracted Flood ID: {flood_id}")
            
            # Fetch flood data for the extracted ID
            flood_data = get_flood_by_id(flood_id)
            if flood_data:
                print(f"\nFlood data for ID {flood_id}:")
                print(json.dumps(flood_data, indent=2))
            else:
                print(f"No data available for flood ID {flood_id}")
        else:
            print("No flood warnings available")
        
        # Example coordinates (latitude, longitude) and radius in km
        lat, long, radius = 51.5074, -0.1278, 10
        stations = get_stations_near_coordinates(lat, long, radius)
        if stations:
            save_to_csv(stations, "data/stations.csv")
            print(f"\nStations near ({lat}, {long}) within {radius} km radius:")
            print(pd.DataFrame(stations).head())
        else:
            print(f"No stations available near coordinates ({lat}, {long}) within {radius} km radius")
        
        # Fetch flood data for a specific flood area ID (example: "122WAC953")
        specific_flood_id = "122WAC953"
        specific_flood_data = get_flood_by_id(specific_flood_id)
        if specific_flood_data:
            print(f"\nSpecific flood data for ID {specific_flood_id}:")
            print(json.dumps(specific_flood_data, indent=2))
        else:
            print(f"No data available for specific flood ID {specific_flood_id}")

        # Wait for 10 minutes before fetching the data again
        time.sleep(60)

# Run the main function
if __name__ == "__main__":
    main()