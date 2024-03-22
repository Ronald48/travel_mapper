import requests
import json

url = "http://datamall2.mytransport.sg/ltaodataservice/TrafficIncidents"

payload = {}
headers = {
  'AccountKey': 'fzkBxinhRzGjwp9Z8nerng==',
  'accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)
data_dict = response.json()

# Initialize a dictionary to store latitudes, longitudes, and messages
incidents_dict = {}
i = 0
incident_type_list = [
    'Accident',
    'Road Works',
    'Vehicle Breakdown',
    'Weather',
    'Obstacle',
    'Road Block',
    'Heavy Traffic',
    'Misc.',
    'Diversion',
    'Unattended Vehicle'
]


# Iterate over the incidents and store them in the dictionary
for incident in data_dict['value']:
    latitude = incident['Latitude']
    longitude = incident['Longitude']

    # filter out nature of the message
    message = incident['Message']
    for incident_type in incident_type_list:
    # Check if the category appears in the sample string
        if incident_type.lower() in message.lower():
            category = incident_type
            break

    incidents_dict[i] = {'Latitude': latitude, 'Longitude': longitude, 'Type': category}
    i += 1

# Print the resulting dictionary of dictionaries
for key, value in incidents_dict.items():
    print(key, ":", value)
