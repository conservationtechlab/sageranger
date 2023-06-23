import requests
from datetime import datetime
Headers = {
        'X-CSRFToken': 'fbnRqkjjGGsAYvRKlN2drA3X9SgIx3OrZkUyN4tFuQ9ADOUdGxYmPcaDfKZQwJln',
        'Authorization':'Bearer iJfzvY8xM9EeG85bGAUygBvYwRB0pq',
        'Accept':'application/json'
   }
#post observations monthly to ensure every camera trap stays active on earth ranger
url1 = 'https://sagebrush.pamdas.org/api/v1.0/observations/'
url2 = 'https://sagebrush.pamdas.org/api/v1.0/sources/'
current_time = datetime.utcnow()
formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

response = requests.get (url2, headers=Headers)
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
		requests.post(url1, headers=Headers, json=obs_data)
