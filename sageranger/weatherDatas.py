import requests
import pandas as pd
import csv
import json
import datetime
from datetime import timezone
from time import gmtime, strftime


Headers = {
     'X-CSRFToken': 'Token API',
     'Authorization': 'Bearer Authorization'
}

#URL
url = 'https://sagebrush.pamdas.org/api/v1.0/observations/?subject_id=ee76e226-c05e-400b-9ae9-db8b11b5359b'



def get_sensor(token, autorization):
    '''This function posts observation on the heat sensor'''
    Headers = {
            'X-CSRFToken': token,
            'Authorization': autorization,
    }
  
    

response= requests.get(url, headers=Headers, timeout=20)

json_string = response.content


# Load the JSON data
data = json.loads(json_string)



#Check network connection
print(response)

def extract_results(data):
    result_list = []
    
    for i in range(0, len(data['data']['results'])):
        result = data['data']['results'][i]
        result_list.append(result)
    
    return pd.DataFrame(result_list)

df = extract_results(data)

print(df)
first_df = df[['id', 'recorded_at', 'created_at', 'source', 'exclusion_flags']]
print(first_df)

# Extracting longitude and latitude data
def location(data):
    results = data['data']['results']
    location_df = pd.DataFrame(results)
    location_df['longitude'] = location_df['location'].apply(lambda x: x['longitude'])
    location_df['latitude'] =location_df['location'].apply(lambda x: x['latitude'])
    location_df = (location_df[['longitude', 'latitude']])
    return location_df



def device_status_properties(data):
    cols = {'Humidity': 0, 'External Temperature': 1 , 'Internal Temperature': 2, 'Battery Status': 3}
    dataSet = []  # Initialize an empty list to store the results
    
    for row in df['device_status_properties'].values:
        x = ['0%', '0C', '0C', '0V']
        if type(row) == list:
            for val in row:
                colKey = val['label']
                value = str(val['value'])
                # Replace the 0 in the row with the value in the value column
                x[cols[colKey]] = x[cols[colKey]].replace('0', str(value))
        dataSet.append(x)
    device_df = pd.DataFrame(dataSet, columns = cols)
    return device_df

print(device_status_properties(data))

#Concate for row and column
def concat_df(df1, df2, df3):
     concatenated_df = pd.concat([df1, df3,df2], axis=1)
     return concatenated_df
    

second_df = device_status_properties(data)
third_df = location(data)
result_df = concat_df(first_df, second_df, third_df)

result_df.to_csv('weatherReport.csv', index=False)

