import os
import requests
import json
import random
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        # self.container_name = os.getenv('AZURE_CONTAINER_NAME')
        self.account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
        self.account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
        self.container_name = f"openweather{random.randint(1000, 9999)}"

 
    def create_azure_container(self):
        try:
            # Construct the connection string
            connection_string = (
                f"DefaultEndpointsProtocol=https;"
                f"AccountName={self.account_name};"
                f"AccountKey={self.account_key};"
                f"EndpointSuffix=core.windows.net"
            )
            
            # Create the BlobServiceClient
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            
            # Create the container
            container_client = blob_service_client.create_container(self.container_name)

            if not container_client.exists():
                blob_service_client.create_container(self.container_name)
                print(f"Container '{self.container_name}' created successfully!")
            else:
                print(f"Container '{self.container_name}' already exists.")
        except Exception as e:
            print(f"Failed to create container: {e}")


    def fetch_weather(self, city):
        # Fetch weather data from OpenWeather API
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        

    def save_data_to_azure(self, data, city):
        try:
            # Construct the connection string
            connection_string = (
                f"DefaultEndpointsProtocol=https;"
                f"AccountName={self.account_name};"
                f"AccountKey={self.account_key};"
                f"EndpointSuffix=core.windows.net"
            )
            
            # Create BlobServiceClient
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            
            # Get the container client
            container_client = blob_service_client.get_container_client(self.container_name)

            if not data:
                return False
            
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            blob_name = f"weather-data/{city}-{timestamp}.json"
            
            # Get the blob client
            blob_client = container_client.get_blob_client(blob_name)
            
            # Upload the data
            if isinstance(data, dict):
                data = json.dumps(data)
            blob_client.upload_blob(data, overwrite=True)
            print(f"Data uploaded to blob '{blob_name}' in container '{self.container_name}'.")
        except Exception as e:
            print(f"Failed to upload data: {e}")

        


def main():
    try:
        dashboard = WeatherDashboard()

        # create azure container
        dashboard.create_azure_container()

        # List of cities to track
        cities = ["London", "York", "Liverpool"]

        for city in cities:
            print(f"\nProcessing weather data for {city}")
            weather_data = dashboard.fetch_weather(city)
            if weather_data:
                dashboard.save_data_to_azure(weather_data, city)
                print(f"Successfully processed {city}")
            else:
                print(f"Failed to process {city}")

    except Exception as e:
        print(f"Main execution failed: {e}")


if __name__ == "__main__":
    main()