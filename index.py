import requests
import pandas as pd
import json
import time
import matplotlib.pyplot as plt

# Define the base URL for the API
base_url = "http://environment.data.gov.uk/flood-monitoring"
print('base_url', base_url)

# Function to get water level readings from all measurement stations
def get_water_level_readings():
    url = f"{base_url}/data/readings?parameter=waterLevel"
    response = requests.get(url)
    print('response', response)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        print("Failed to retrieve water level data")
        return None

# Function to get flow rate readings from all measurement stations
def get_flow_rate_readings():
    url = f"{base_url}/data/readings?parameter=flow"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        print("Failed to retrieve flow rate data")
        return None

# Function to get rainfall data
def get_rainfall_data():
    url = f"{base_url}/data/readings?parameter=rainfall"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        print("Failed to retrieve rainfall data")
        return None

# Function to visualize water level readings
def visualize_water_level_readings(readings):
    df = pd.DataFrame(readings)
    plt.plot(df['dateTime'], df['value'], marker='o')
    plt.xlabel('Date and Time')
    plt.ylabel('Water Level')
    plt.title('Water Level Readings')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))  # Adjust the number of ticks as needed
    plt.tight_layout()
    plt.show()

# Function to visualize flow rate readings
def visualize_flow_rate_readings(readings):
    df = pd.DataFrame(readings)
    plt.plot(df['dateTime'], df['value'], marker='o')
    plt.xlabel('Date and Time')
    plt.ylabel('Flow Rate')
    plt.title('Flow Rate Readings')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))  # Adjust the number of ticks as needed
    plt.tight_layout()
    plt.show()

# Function to visualize rainfall data
def visualize_rainfall_data(data):
    df = pd.DataFrame(data)
    plt.plot(df['dateTime'], df['value'], marker='o')
    plt.xlabel('Date and Time')
    plt.ylabel('Rainfall (mm)')
    plt.title('Rainfall Data')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))  # Adjust the number of ticks as needed
    plt.tight_layout()
    plt.show()

# Function to save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to fetch and display data
def main():
    print("Starting the data retrieval process")
    while True:
        # Fetch water level readings
        print('fetching water level readings')
        water_level_readings = get_water_level_readings()
        if water_level_readings:
            save_to_csv(water_level_readings, "data/water_level_readings.csv")
            visualize_water_level_readings(water_level_readings)
        else:
            print("No water level readings available")

        # Fetch flow rate readings
        flow_rate_readings = get_flow_rate_readings()
        if flow_rate_readings:
            save_to_csv(flow_rate_readings, "data/flow_rate_readings.csv")
            visualize_flow_rate_readings(flow_rate_readings)
        else:
            print("No flow rate readings available")

        # Fetch rainfall data
        rainfall_data = get_rainfall_data()
        if rainfall_data:
            save_to_csv(rainfall_data, "data/rainfall_data.csv")
            visualize_rainfall_data(rainfall_data)
        else:
            print("No rainfall data available")

        # Include retrieval of flood warnings and river basin characteristics if available

        # Wait for 10 minutes before fetching the data again
        time.sleep(60)  # Increase to 10 minutes

# Run the main function
if __name__ == "__main__":
    main()