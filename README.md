# Azure Weather Dashboard 🌦️

## Overview
This project is part of the **30 Days DevOps Challenge** `#DevOpsAllStarsChallenge`  
**Day 1** focuses on integrating weather data from the OpenWeather API with Azure Blob Storage.

The **Azure Weather Dashboard** is a Python-based project designed to fetch real-time weather data for specified cities using the OpenWeather API and store this data in Azure Blob Storage. This project demonstrates the integration of third-party APIs with Azure Storage and showcases scalable and automated data storage solutions.

---

## Features
- **Fetch Real-Time Weather Data**: Retrieve current weather details (e.g., temperature, humidity, weather conditions) for multiple cities.
- **Dynamic Azure Blob Storage**: Automatically create uniquely named Azure Blob Storage containers to store data.
- **Seamless Integration**: Securely connect to Azure Storage and interact programmatically.
- **JSON Data Storage**: Save weather data in a structured JSON format for easy retrieval and processing.

---

## Requirements

### Python Libraries
- `azure-storage-blob`
- `requests`
- `python-dotenv`

### Environment Variables
Create a `.env` file in the project directory with the following variables:

#### OpenWeather API
```
OPENWEATHER_API_KEY=your_openweather_api_key
```

#### Azure Storage
In a resource group in the Azure Portal, Set up a Storage Account and obtain the Storage Account Name and Access Key
```
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
AZURE_STORAGE_ACCOUNT_KEY=your_storage_account_key
```

## Installation
```
git clone git https://github.com/peymosiec01/Day-1---Weather-Dashboard-with-Azure-Storage.git
cd weather-dashboard-demo
```

## Install dependencies:
```python
pip install -r requirements.txt
```
Add the .env file to the root directory with the required variables.

## Usage
Run the script to fetch weather data and upload it to Azure Blob Storage:
```python
python weather_dashboard.py
```

## Code Highlights
### 1. Weather API Integration
The project fetches weather data using the OpenWeather API:

```python
def fetch_weather(self, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": self.api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    return response.json()
```

### 2. Dynamic Azure Container Creation
Creates a unique Azure container:
```python
self.container_name = f"openweather{random.randint(1000, 9999)}"
```

### 3. Storing Data in Azure
Weather data is saved in JSON format:
```python
blob_client.upload_blob(json.dumps(data), overwrite=True)
```

```
Processing weather data for London
Container 'openweather8465' created successfully!
Data uploaded to blob 'weather-data/London-20250106-123456.json' in container 'openweather8465'.

Processing weather data for York
Data uploaded to blob 'weather-data/York-20250106-123459.json' in container 'openweather8465'.
```
![image](https://github.com/user-attachments/assets/487dee4a-aa17-4ef4-b59c-f0122ac39615)
![image](https://github.com/user-attachments/assets/e04cb3f0-91f7-44ab-8916-e3013b6801bf)

## License
This project is licensed under the MIT License. See the LICENSE file for details.
