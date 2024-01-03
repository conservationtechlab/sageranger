
import pandas as pd
import requests
import json
import pytz
import datetime
from datetime import datetime, timedelta, timezone

from time import gmtime, strftime


Headers = {
     'X-CSRFToken': 'IfmhCe09jkTbCl2Rc5lCmNlzepp1GFQncHJNSgTbslZtashIMtByyAlMpYIx1Xcp',
     'Authorization': 'Bearer I4xBKwEBK7h7FxtpdBHyc4XkWCCuJM'
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


def extract_results(data):
    result_list = []
    
    for i in range(0, len(data['data']['results'])):
        result = data['data']['results'][i]
        result_list.append(result)
    
    return pd.DataFrame(result_list)

df = extract_results(data)

# df['recorded_at'] = pd.to_datetime(df['recorded_at'], utc=True)

# # Convert to PST (Pacific Standard Time)
# df['recorded_at_pst'] = df['recorded_at'].dt.tz_convert('America/Los_Angeles')

# # Format the 'recorded_at_pst' column with US standard time format
# df['formatted_time'] = df['recorded_at_pst'].dt.strftime('%Y-%m-%d %I:%M:%S %p')
# pst_time = df['formatted_time']
# print(pst_time)

# Function to check if a date string is within the last week
# def is_last_week(data):
#     date_obj = datetime.fromisoformat(data[:-6])  # Removing the timezone offset for simplicity
#     last_week = datetime.now() - timedelta(days=7)
#     return date_obj >= last_week

##################################################################
#   Define the start and end dates for your desired date range
#   for your report.
#      
##################################################################

start_date = datetime(2023, 4, 1, tzinfo=pytz.UTC)
end_date = datetime(2023, 4, 30, tzinfo=pytz.UTC)


# Extracting data form (exclude exclusion_flags)
first_df = df[['id','recorded_at','created_at', 'source']]
#print(first_df)

# Extracting data from longitude and latitude
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

#print(device_status_properties(data))

#Concate for row and column
def concat_df(df1, df2, df3):
     concatenated_df = pd.concat([df1, df3,df2], axis=1)
     return concatenated_df
    

second_df = device_status_properties(data)
third_df = location(data)
# Concatenate DataFrames
result_df = concat_df(first_df, second_df, third_df)

    
def filter_and_save_to_csv(result_df, start_date, end_date, output_filename):
        title = f'From_{start_date.strftime("%Y%m%d")}_To_{end_date.strftime("%Y%m%d")}'
        # Convert 'recorded_at' to datetime format
        result_df['recorded_at'] = pd.to_datetime(result_df['recorded_at']).dt.tz_convert('America/Los_Angeles')
        # Filter data based on the date range
        filtered_df = result_df[(result_df['recorded_at'] >= start_date) & (result_df['recorded_at'] <= end_date)]
       
       # Save to CSV with title as the first row
        with open(output_filename, 'w', newline='') as file:
            file.write(f'Date: {title}\n')
            filtered_df.to_csv(file, index=False)

output_filename = 'temperatureReport.csv'

# Call the function
filter_and_save_to_csv(result_df, start_date, end_date, output_filename)



