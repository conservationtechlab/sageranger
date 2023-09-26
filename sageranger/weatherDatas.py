import requests
import pandas as pd
import csv
import json
import datetime
from datetime import timezone
from time import gmtime, strftime

Headers = {
     'X-CSRFToken': 'token',
     'Authorization': 'Bearer Authorization'
}


url = 'https://sagebrush.pamdas.org/api/v1.0/observations/?subject_id=ee76e226-c05e-400b-9ae9-db8b11b5359b'


   
response= requests.get(url, headers=Headers, timeout=20)

data = response.json().get("results", []) or []



 
def extract_property_value(properties, prop_name):
    if not isinstance(properties, list):
        return "0"
    return next((prop["value"] for prop in properties if isinstance(prop, dict) and prop.get("name")== prop_name), '0')


df = pd.DataFrame({
    'humidity': [extract_property_value(obs['device_status_properties'], 'humidity') for obs in data],
    'recorded_at': [obs.get['recorded_at','0'] for obs in data],
    'battery': [extract_property_value(obs['device_status_properties'], 'battery')for obs in data],
    'external_temperature': [extract_property_value(obs['device_status_properties'],'external_temperature')for obs in data],
    'internal_temperature': [extract_property_value(obs['device_status_properties'],'internal_temperature')for obs in data]
})

# Print the dataframe
print(df)




# def get_date(df):
#     # Getting key
#     recorded_at_key = list(df['data']['results'][0].keys())[2]

#     print(recorded_at_key.capitalize())

#     # Getting all the recorded_at value
#     recorded_at = [df['data'][3][i][recorded_at_key] for i in range(0, len(df['data'][3]))]


#     for index, time in enumerate(recorded_at):
        
#         # Convert recorded_at to datetime format
#         new_timestamp = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        
#         #converts the new_timestamp object to GMT.
#         new_timestamp_gmt = new_timestamp.astimezone(timezone.utc)
        
#         # Format new_timestamp_gmt in GMT
#         new_timestamp_gmt_formatted = new_timestamp_gmt.strftime("%A, %Y-%m-%d %H:%M:%S")
        
#         dates_list = ('Timestamp: ', new_timestamp_gmt_formatted)
        
#         print(dates_list)
        
#     return dates_list

# print(get_date(df))






  
  
