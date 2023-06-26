import requests
from datetime import datetime as dt
import yaml

def post_monthly_obs(TOKEN, AUTH):

	Headers = {
		'X-CSRFToken': TOKEN,
       	'Authorization':AUTH,
        	'Accept':'application/json'
   	}
	
	url_obs = 'https://sagebrush.pamdas.org/api/v1.0/observations/'
	url_s = 'https://sagebrush.pamdas.org/api/v1.0/sources/'

	current_time = dt.utcnow()
	formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

	response = requests.get (url_s, headers=Headers)
	response_json=response.json()
	results=response_json['data']['results']

	for i in range(len(results)):
		if results[i]['manufacturer_id'][:2]=='B0':
			obs_data = {
	 			"location": {"longitude": 0, "latitude": 0}, 
				"recorded_at": formatted_time, 
				"source": results[i]['id'], 
	 			"device_status_properties": [{"value": 'test', "label": "animal", "units": ""}], 
	 			"additional": {"animal": 'test'}}
			response = requests.post(url_obs, headers=Headers, json=obs_data)
			print(response)
